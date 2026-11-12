use std::{
    sync::{
        Arc,
        atomic::{AtomicUsize, Ordering},
    },
    time::Duration,
};

use base64::{Engine, engine::general_purpose::STANDARD};
use linten_core_utils::settings::Lookup;
use linten_http::{HttpClientPool, HttpSettings, Resolution, media::PublicDnsResolver};
use linten_secret_value::SecretValue;
use linten_secrets_cyberark::{CyberArkSecretManager, DeleteOutcome, Error};
use linten_secrets_types::{BaseSecretManager, CyberarkOperationContext};

use rstest::{fixture, rstest};
use serde::Deserialize;
use wiremock::{
    Match, Mock, MockServer, Request, ResponseTemplate,
    matchers::{body_string, header, method, path},
};

#[path = "secret_manager/support.rs"]
mod support;
use support::*;

#[path = "secret_manager/configuration.rs"]
mod configuration;
#[path = "secret_manager/reads.rs"]
mod reads;
#[path = "secret_manager/writes.rs"]
mod writes;
