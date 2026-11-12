#[derive(Default)]
pub struct AuthServices {
    #[cfg(feature = "aws")]
    pub aws: linten_auth_aws::AwsAuthService,
    #[cfg(feature = "azure")]
    pub azure: linten_auth_azure::AzureAuthService,
    #[cfg(feature = "gcp")]
    pub gcp: linten_auth_gcp::VertexAuth,
}
