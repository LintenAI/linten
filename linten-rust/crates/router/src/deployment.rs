use std::time::Duration;

use linten_inference_messages::MessagesShaping;
use linten_router_types::LintenParams;

#[derive(Clone, Debug, Default)]
pub struct Deployment {
    pub model: String,
    pub api_key: Option<String>,
    pub api_base: Option<String>,
    pub custom_llm_provider: Option<String>,
    pub linten_params: LintenParams,
    pub timeout: Option<Duration>,
    pub shaping: MessagesShaping,
}
