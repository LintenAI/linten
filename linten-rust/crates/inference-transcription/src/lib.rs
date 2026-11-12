pub mod types;
pub use linten_inference::Error;
mod constants;
mod handler;

use linten_auth::AuthServices;
use linten_core_utils::get_llm_provider_logic::LlmProviders;
use linten_inference::provider::resolve_llm_provider;
use linten_llms::{
    base_llm::audio_transcription::transformation::BaseAudioTranscriptionConfig,
    bedrock::audio_transcription::BEDROCK_AUDIO_TRANSCRIPTION_CONFIG,
};
use linten_secrets::source::SecretSource;
use serde_json::Value;
use std::sync::Arc;

use crate::types::AudioTranscriptionRequest;

fn audio_transcription_provider(
    provider: LlmProviders,
) -> Option<&'static dyn BaseAudioTranscriptionConfig> {
    match provider {
        LlmProviders::Bedrock => Some(&BEDROCK_AUDIO_TRANSCRIPTION_CONFIG),
        _ => None,
    }
}

#[derive(Clone)]
pub struct AudioTranscriptionRoute {
    http: linten_http::Client,
    auth: Arc<AuthServices>,
    secrets: Arc<dyn SecretSource>,
}

impl AudioTranscriptionRoute {
    pub fn new(
        http: linten_http::Client,
        auth: Arc<AuthServices>,
        secrets: Arc<dyn SecretSource>,
    ) -> Self {
        Self {
            http,
            auth,
            secrets,
        }
    }

    pub async fn execute(&self, request: AudioTranscriptionRequest<'_>) -> Result<Value, Error> {
        self.run(request).await
    }

    #[tracing::instrument(name = "linten.route", skip_all, fields(
        route = "audio_transcription",
        model = request.model,
        provider,
        resolved_model,
        stream = false,
        outcome
    ))]
    async fn run(&self, request: AudioTranscriptionRequest<'_>) -> Result<Value, Error> {
        linten_inference::diagnostic::unary(async {
            let provider = resolve_llm_provider(
                request.model,
                request.custom_llm_provider,
                "audio transcription",
            )?;
            let config = audio_transcription_provider(provider.provider).ok_or_else(|| {
                Error::InvalidProvider(<&str>::from(provider.provider).to_string())
            })?;
            linten_inference::diagnostic::provider(
                provider.model,
                <&'static str>::from(provider.provider),
            );
            let secrets = self.secrets.resolve(&config.secret_names()).await?;
            let execute: futures_util::future::BoxFuture<'_, Result<Value, Error>> = Box::pin(
                handler::execute(&self.http, &self.auth, config, provider, request, secrets),
            );
            execute.await
        })
        .await
    }
}
