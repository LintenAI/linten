mod common_utils;
mod constants;
mod handler;
pub mod route;
mod types;

use futures_util::FutureExt;
use linten_auth::AuthServices;
use linten_host::interceptors::Interceptors;
use linten_inference::context::CallContext;
use linten_inference::provider::resolve_llm_provider;
use linten_secrets::source::SecretSource;
use std::sync::Arc;

use crate::common_utils::messages_provider;

pub use common_utils::merge_messages_header_sources;
pub use linten_inference::Error;
pub use types::{
    MessagesBody, MessagesCall, MessagesCallResponse, MessagesSettings, MessagesShaping,
    linten_params, messages_body,
};

#[derive(Clone)]
pub struct MessagesRoute {
    http: linten_http::Client,
    auth: Arc<AuthServices>,
    secrets: Arc<dyn SecretSource>,
    cache: Option<linten_cache_response::ScopedCache>,
}

impl MessagesRoute {
    pub fn new(
        http: linten_http::Client,
        auth: Arc<AuthServices>,
        secrets: Arc<dyn SecretSource>,
    ) -> Self {
        Self {
            http,
            auth,
            secrets,
            cache: None,
        }
    }

    #[must_use]
    pub fn with_cache(self, cache: linten_cache_response::ScopedCache) -> Self {
        Self {
            cache: Some(cache),
            ..self
        }
    }

    pub async fn execute(
        &self,
        call: MessagesCall,
        interceptors: &impl linten_host::interceptors::Interceptors<Error>,
        options: impl Into<linten_inference::CallOptions>,
    ) -> Result<MessagesCallResponse, Error> {
        let context = CallContext::new(interceptors, options.into());
        linten_host::lifecycle::observe_call(context.observers.clone(), self.run(call, context))
            .await
    }

    #[tracing::instrument(name = "linten.route", skip_all, fields(
        route = "messages",
        model = %call.body.model,
        provider,
        resolved_model,
        stream = call.body.params.stream == Some(true),
        outcome
    ))]
    async fn run(
        &self,
        call: MessagesCall,
        context: CallContext<'_, impl Interceptors<Error>>,
    ) -> Result<MessagesCallResponse, Error> {
        linten_inference::diagnostic::call(async {
            let provider = resolve_llm_provider(
                &call.body.model,
                call.custom_llm_provider.as_deref(),
                "messages",
            )?;
            let config = messages_provider(provider.provider, provider.model).ok_or_else(|| {
                Error::InvalidProvider(<&str>::from(provider.provider).to_string())
            })?;
            linten_inference::diagnostic::provider(
                provider.model,
                <&'static str>::from(provider.provider),
            );
            let model = provider.model.to_owned();
            let secrets = self.secrets.resolve(config.config().secret_names()).await?;
            handler::execute(self, config, model, call, secrets, &context)
                .boxed()
                .await
        })
        .await
    }
}
