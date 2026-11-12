use std::sync::Arc;

use linten_auth::AuthServices;
use linten_http::HttpClientPool;

#[derive(Clone)]
pub struct CoreResources {
    pub pool: Arc<HttpClientPool>,
    pub auth: Arc<AuthServices>,
}

impl CoreResources {
    pub fn new(pool: Arc<HttpClientPool>) -> Self {
        Self {
            pool,
            auth: Arc::new(AuthServices::default()),
        }
    }
}
