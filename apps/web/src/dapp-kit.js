// src/dapp-kit.js
import { createDAppKit } from '@mysten/dapp-kit-core';
import { SuiGrpcClient } from '@mysten/sui/grpc';

const GRPC_URLS = {
    testnet: 'https://fullnode.testnet.sui.io:443',
    // 也可以添加 mainnet 或 devnet
};

export const dAppKit = createDAppKit({
    networks: ['testnet'], // 声明你的应用支持的网络
    createClient: (network) => new SuiGrpcClient({ 
        network, 
        baseUrl: GRPC_URLS[network] 
    }),
});