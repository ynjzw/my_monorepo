<script setup >
import { useStore } from '@nanostores/vue';
import { Transaction } from "@mysten/sui/src/transactions";
import { dAppKit } from '../dapp-kit';

// 使用 nanostores 响应式获取连接状态
const connection = useStore(dAppKit.stores.$connection);

// 发送交易的函数
async function handleTransfer() {
  if (!connection.value.account) return;

  const tx = new Transaction();
  
  // 示例1：调用 Move 合约函数
  tx.moveCall({
    target: `0x你的包ID::模块名::函数名`,
    arguments: [
      // 根据你的函数签名传入参数，例如：
      // tx.pure.string("hello"),
      // tx.object("0x对象ID"),
    ],
  });

  // 示例2：直接转账 1 SUI（如果需要）
//   tx.transferObjects(
//     [coinWithBalance({ balance: 1_000_000 })], // 1 SUI = 1,000,000 MIST
//     connection.value.account.address
//   );

  try {
    const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });
    
    if (result.FailedTransaction) {
      throw new Error(`交易失败: ${result.FailedTransaction.status.error?.message}`);
    }
    
    alert(`交易成功！Digest: ${result.Transaction.digest}`);
  } catch (error) {
    console.error('交易失败:', error);
  }
}
</script>

<template>
  <div>
    <h1>我的 Sui dApp</h1>
    <!-- 官方的钱包连接按钮 Web Component -->
    <mysten-dapp-kit-connect-button :instance="dAppKit" />

    <div v-if="connection.account">
      <p>地址: {{ connection.account.address }}</p>
      <button @click="handleTransfer">发送交易</button>
    </div>
    <p v-else>请先连接钱包</p>
  </div>
</template>