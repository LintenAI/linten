# morselaunch contracts

One transaction deploys a fixed-supply ERC-20, opens a Uniswap v4 pool, and locks the whole supply as liquidity. The factory and the locker have no owner, no admin, and no fee address. A creator chooses a trading fee of 0%, 1%, or 3%. That fee is paid to the beneficiaries named at launch, or burned.

The site is [morselaunch.xyz](https://morselaunch.xyz). This repository is the Foundry project for the contracts. The site is [MorseLaunch/app](https://github.com/MorseLaunch/app). Notes are in [MorseLaunch/docs](https://github.com/MorseLaunch/docs).

## Contracts

| Contract | Role |
|---|---|
| `src/LaunchFactory.sol` | Deploys the token, initializes one v4 pool, and mints a single-sided position for the full supply. |
| `src/LaunchFactoryArc.sol` | The same factory, plus a guard that refuses a native-asset quote. Arc deploys this copy. The Base source is not edited. |
| `src/LaunchLocker.sol` | Holds every position NFT. There is no transfer, decrease, or burn path. `collect` pushes fees to the recipients fixed at launch. |
| `src/LaunchToken.sol` | ERC-20 with permit. No mint, pause, blacklist, or tax. |

`collect` is permissionless. Recipients cannot be changed after launch. A recipient that cannot receive the payout is credited and can claim later. Design notes, events, and the invariants the indexer relies on are in [`docs/LAUNCHPAD.md`](docs/LAUNCHPAD.md).

## Live deployments

Base, Robinhood Chain, and Arc share one factory and one locker. BNB Smart Chain and Elysium were deployed later, from the same `LaunchFactory` source, at new addresses. Records are in `deployments/`.

| Chain | Factory | Locker |
|---|---|---|
| Base (8453) | [`0x815542E8b392389A1389E22E588E4B62A67Ade72`](https://basescan.org/address/0x815542E8b392389A1389E22E588E4B62A67Ade72#code) | [`0xcd1680D26922fcd9CabFbb8a56bA40C333fD842a`](https://basescan.org/address/0xcd1680D26922fcd9CabFbb8a56bA40C333fD842a#code) |
| Robinhood Chain (4663) | [`0x815542E8b392389A1389E22E588E4B62A67Ade72`](https://robinhoodchain.blockscout.com/address/0x815542E8b392389A1389E22E588E4B62A67Ade72) | [`0xcd1680D26922fcd9CabFbb8a56bA40C333fD842a`](https://robinhoodchain.blockscout.com/address/0xcd1680D26922fcd9CabFbb8a56bA40C333fD842a) |
| Arc (5042) | [`0x815542E8b392389A1389E22E588E4B62A67Ade72`](https://explorer.arc.io/address/0x815542E8b392389A1389E22E588E4B62A67Ade72) | [`0xcd1680D26922fcd9CabFbb8a56bA40C333fD842a`](https://explorer.arc.io/address/0xcd1680D26922fcd9CabFbb8a56bA40C333fD842a) |
| BNB Smart Chain (56) | [`0xE69B7098825437c6504811eA6f905A38F3719a0e`](https://bscscan.com/address/0xE69B7098825437c6504811eA6f905A38F3719a0e) | [`0x2568fEBfDaC4848dF32B16Ab0FfcB07D44881d87`](https://bscscan.com/address/0x2568fEBfDaC4848dF32B16Ab0FfcB07D44881d87) |
| Elysium (99901) | [`0x44db53C69356201867B36DCF46d6C925AB012945`](https://elyscan.live/address/0x44db53C69356201867B36DCF46d6C925AB012945) | [`0x194B634e673775C870Ca6C48F82F1A1E357D78CA`](https://elyscan.live/address/0x194B634e673775C870Ca6C48F82F1A1E357D78CA) |

On Arc the factory bytecode is `LaunchFactoryArc`. The locker is the same contract on every chain. `deployed.lock` pins the source and the library commits that match the verified Base, Robinhood Chain, and Arc deployments.

## Build and test

Foundry, Solidity 0.8.26, Cancun, via IR, optimizer 200. Uniswap v4 and forge-std are submodules.

```bash
git submodule update --init --recursive
forge test --match-path test/LaunchFactory.t.sol
forge test --match-contract LaunchEventsTest
```

Fork tests read a live chain and stay off unless `FORK_TESTS=true`. Put RPC URLs in `.env`, which is gitignored. `.env.example` lists the names.

```bash
FORK_TESTS=true forge test --match-contract LaunchLockerRugFork
FORK_TESTS=true forge test --match-contract LaunchStockQuote
FOUNDRY_PROFILE=arc FORK_TESTS=true arc-forge test --match-contract LaunchFactoryArcFork
```

The Arc fork suite needs [circlefin/arc-foundry](https://github.com/circlefin/arc-foundry). Upstream `forge` cannot execute Arc USDC transfers.

`forge build` writes `out/`, and a broadcast writes `broadcast/` and `cache/`. Those directories are gitignored.

## Deploy

A new chain needs its Uniswap v4 PoolManager and PositionManager. Base, Robinhood Chain, and Arc are hard-coded in `script/DeployLaunchFactory.s.sol`. Any other chain must set `POOL_MANAGER` and `POSITION_MANAGER`. Arc deploys `LaunchFactoryArc`. Every other chain deploys `LaunchFactory`.

Copy `.env.example` to `.env` and set `DEPLOYER_PRIVATE_KEY` there. Do not commit it. The key pays gas and keeps no privilege after the constructor.

```bash
forge script script/DeployLaunchFactory.s.sol --rpc-url "$BASE_RPC_URL" --broadcast
```

Verify with `script/verify.sh`. Constructor arguments are PoolManager, PositionManager, and Permit2 for the factory, and PositionManager for the locker. Permit2 is `0x000000000022D473030F116dDEE9F6B43aC78BA3`.

## License

MIT. Keep the copyright and permission notice with any copy. The site is [MorseLaunch/app](https://github.com/MorseLaunch/app). Notes are in [MorseLaunch/docs](https://github.com/MorseLaunch/docs).
