pub mod arguments;
pub mod document;
pub(crate) mod handler;
pub mod provider_config;
pub mod route;
pub mod types;
pub mod wire;

use std::sync::Arc;

use linten_host::interceptors::Interceptors;
use linten_host::observation::ObservationSender;
use linten_llms::base_llm::ocr::{error::Error, handler::OcrClient};
use linten_llms_types::formats::ocr::LintenOcrResponse;

use crate::{
    handler::execute,
    types::{LintenOcrRequest, OcrDocumentInput},
};

#[derive(Clone)]
pub struct OcrRoute {
    client: OcrClient,
}

impl OcrRoute {
    pub fn new(client: OcrClient) -> Self {
        Self { client }
    }

    pub async fn execute(
        &self,
        request: LintenOcrRequest,
        interceptors: &impl Interceptors<Error>,
        observers: Option<ObservationSender>,
    ) -> Result<LintenOcrResponse, Error> {
        linten_host::lifecycle::observe_unary(
            observers.clone(),
            self.run(request, interceptors, observers.as_ref()),
        )
        .await
    }

    #[tracing::instrument(name = "linten.route", skip_all, fields(
        route = "ocr",
        model = %call.model,
        resolved_model = %call.model,
        provider = <&str>::from(call.config.provider()),
        stream = false,
        outcome
    ))]
    async fn run(
        &self,
        call: LintenOcrRequest,
        interceptors: &impl Interceptors<Error>,
        observers: Option<&ObservationSender>,
    ) -> Result<LintenOcrResponse, Error> {
        linten_inference::diagnostic::unary(async {
            let caller_document = matches!(&call.document, OcrDocumentInput::Document(_));
            let call = document::resolve_document(call).await?;
            let config = call.config;
            let secrets = self
                .client
                .secret_source()
                .resolve(&config.secret_names())
                .await
                .map_err(|error| Error::Secret(Arc::new(error)))?;
            let execute: futures_util::future::BoxFuture<'_, Result<LintenOcrResponse, Error>> =
                Box::pin(execute(
                    &self.client,
                    config,
                    call,
                    secrets,
                    interceptors,
                    caller_document,
                    observers,
                ));
            execute.await
        })
        .await
    }
}
