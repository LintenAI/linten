mod host;

use std::sync::Arc;

use host::ChatCompletionsPythonHost;
use linten_auth::AuthServices;
use linten_cache_response::CachePolicy;
use linten_callbacks_legacy_python::LoggingOperation;
use linten_host::{call::HostedMachine, protocol::Protocol};
use linten_inference_chat::{ChatCompletionsRoute, route::ChatCompletions};
use linten_secrets::source::SecretSource;
use pyo3::prelude::*;

use super::{
    NativeCall,
    inference::{InferenceHost, InferenceRoute, run_inference},
};

fn run_chat_completions(
    py: Python<'_>,
    call: NativeCall<'_>,
    asynchronous: bool,
) -> PyResult<Py<PyAny>> {
    let host = InferenceHost::new(
        call.view()?,
        "linten.rust_bridge.host.routes.chat_completions",
    );
    run_inference::<ChatCompletionsRoute, _>(
        py,
        call,
        asynchronous,
        ChatCompletionsPythonHost(host),
    )
}

#[pyfunction]
pub(crate) fn completion(py: Python<'_>, call: NativeCall<'_>) -> PyResult<Py<PyAny>> {
    run_chat_completions(py, call, false)
}

#[pyfunction]
pub(crate) fn acompletion(py: Python<'_>, call: NativeCall<'_>) -> PyResult<Py<PyAny>> {
    run_chat_completions(py, call, true)
}

impl InferenceRoute for ChatCompletionsRoute {
    type Protocol = ChatCompletions;
    const OPERATION: LoggingOperation = LoggingOperation::Completion;
    const SYNC_CALL_TYPE: &'static str = "completion";
    const ASYNC_CALL_TYPE: &'static str = "acompletion";

    fn new(
        http: linten_http::Client,
        auth: Arc<AuthServices>,
        secrets: Arc<dyn SecretSource>,
    ) -> Self {
        Self::new(http, auth, secrets)
    }

    fn machine(
        self,
        call: <ChatCompletions as Protocol>::Request,
        policy: CachePolicy,
    ) -> HostedMachine<ChatCompletions> {
        self.machine(call, policy)
    }
}
