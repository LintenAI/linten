use linten_auth::{ResolvedCredential, TokenProviderHandle};
use linten_host::observation::ObservationSender;
use linten_host::{
    call::{CallOutput, HostedMachine, hosted_call},
    machine::HostServices,
    protocol::Protocol,
    protocol::Reply,
};
use linten_llms::base_llm::ocr::error::Error;
use linten_llms_types::formats::ocr::LintenOcrResponse;

use crate::types::{LintenOcrRequest, OcrDocumentInput};

pub enum OcrOp {
    AcquireAzureAdToken(Reply<ResolvedCredential>),
}

/// The caller's request as the host projects it.
pub struct OcrCall {
    pub request: LintenOcrRequest<OcrDocumentInput>,
    /// The caller passed its own Azure AD token provider, which the host keeps.
    pub caller_token: bool,
}

pub struct Ocr;

impl Protocol for Ocr {
    type Response = LintenOcrResponse;
    type Error = Error;
    type Request = OcrCall;
    type HostCall = OcrOp;
    type Chunk = std::convert::Infallible;
    type StreamHead = std::convert::Infallible;
}

pub type OcrMachine = HostedMachine<Ocr>;

fn caller_token_provider(services: HostServices<Ocr>) -> TokenProviderHandle {
    TokenProviderHandle::from_callback(move || {
        let host_services = services.clone();
        async move {
            host_services
                .call(OcrOp::AcquireAzureAdToken)
                .await
                .map_err(|error| {
                    linten_auth::Error::CredentialAcquisition(linten_auth::ErrorDetail::failed(
                        "host Azure AD token request",
                        error,
                    ))
                })
        }
    })
}

impl crate::OcrRoute {
    pub fn machine(self, request: OcrCall, observers: Option<ObservationSender>) -> OcrMachine {
        hosted_call(
            request,
            observers,
            move |projection: OcrCall, services, interceptors, observers| async move {
                let request = LintenOcrRequest {
                    azure_ad_token_provider: projection
                        .caller_token
                        .then(|| caller_token_provider(services))
                        .or(projection.request.azure_ad_token_provider),
                    ..projection.request
                };
                self.run(request, &interceptors, observers.as_ref())
                    .await
                    .map(CallOutput::Complete)
            },
        )
    }
}
