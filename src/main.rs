use anyhow::{anyhow, Error};
use cln_plugin::{Builder, Plugin};
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    std::env::set_var("CLN_PLUGIN_LOG", "cln_plugin=info,cln_rpc=info,debug");
    let confplugin = match Builder::new(tokio::io::stdin(), tokio::io::stdout())
        .rpcmethod("qwert", "test", qwert)
        .configure()
        .await?
    {
        Some(plugin) => plugin,
        None => return Err(anyhow!("Error configuring the plugin!")),
    };
    if let Ok(plugin) = confplugin.start(()).await {
        plugin.join().await
    } else {
        Err(anyhow!("Error starting the plugin!"))
    }
}
pub async fn qwert(_p: Plugin<()>, _args: serde_json::Value) -> Result<serde_json::Value, Error> {
    Ok(json!({ "version2": format!("v{}",env!("CARGO_PKG_VERSION")) }))
}
