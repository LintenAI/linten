#![forbid(unsafe_code)]

pub use linten_auth_types::*;

mod services;
pub use services::AuthServices;

#[cfg(feature = "aws")]
pub use linten_auth_aws as aws;
#[cfg(feature = "azure")]
pub use linten_auth_azure as azure;
#[cfg(feature = "gcp")]
pub use linten_auth_gcp as gcp;
