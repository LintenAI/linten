#[derive(Clone, Debug, Default, PartialEq)]
pub struct Namespace(Option<String>);

impl Namespace {
    pub fn new(namespace: impl Into<String>) -> Self {
        let namespace = namespace.into();
        Self((!namespace.is_empty()).then_some(namespace))
    }

    pub fn as_str(&self) -> Option<&str> {
        self.0.as_deref()
    }

    pub(crate) fn apply(&self, key: &str) -> String {
        match &self.0 {
            Some(namespace) if !is_prefixed(key, namespace) => {
                format!("{namespace}:{key}")
            }
            _ => key.to_owned(),
        }
    }
}

fn is_prefixed(key: &str, namespace: &str) -> bool {
    key.strip_prefix(namespace)
        .is_some_and(|rest| rest.starts_with(':'))
}

#[cfg(test)]
mod tests {
    use rstest::rstest;

    use super::Namespace;

    #[rstest]
    #[case::plain(Namespace::new("linten"), "spend:key:abc", "linten:spend:key:abc")]
    #[case::no_namespace(Namespace::default(), "spend:key:abc", "spend:key:abc")]
    #[case::empty_namespace(Namespace::new(""), "spend:key:abc", "spend:key:abc")]
    #[case::already_prefixed(Namespace::new("linten"), "linten:abc", "linten:abc")]
    #[case::shares_prefix_without_delimiter(
        Namespace::new("linten"),
        "linten_spend_update_buffer",
        "linten:linten_spend_update_buffer"
    )]
    #[case::hash_tagged_key(
        Namespace::new("linten"),
        "{api_key:sk-1}:requests",
        "linten:{api_key:sk-1}:requests"
    )]
    fn prefixes_keys_like_python_check_and_fix_namespace(
        #[case] namespace: Namespace,
        #[case] key: &str,
        #[case] expected: &str,
    ) {
        assert_eq!(namespace.apply(key), expected);
    }
}
