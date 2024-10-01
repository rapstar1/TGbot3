function createWallet() {
    // 显示加载动画或禁用按钮，防止重复点击
    document.getElementById('createWallet').disabled = true;

    // 模拟API调用
    fetch('https://tgapp1.onrender.com/api/create-wallet', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('网络响应不正常');
        }
        return response.json();
    }).then(data => {
        console.log(data); // 调试日志
        if (data.address && data.mnemonic) {
            // 将钱包信息插入到中间的容器内，并隐藏按钮
            document.getElementById('walletContainer').innerHTML = `
                <div id="walletInfo">
                    <h2>钱包创建成功！</h2>
                    <p><strong>地址：</strong>${data.address}</p>
                    <p><strong>助记词：</strong>${data.mnemonic}</p>
                    <button class="wallet-btn" onclick="copyMnemonic('${data.mnemonic}')">复制助记词</button>
                    <button class="wallet-btn" onclick="goBack()">返回</button>
                </div>
            `;
        } else {
            alert('创建钱包失败，请重试！');
        }
    }).catch(error => {
        console.error('错误:', error);
        alert('创建钱包失败，请检查网络连接！');
    }).finally(() => {
        // 恢复按钮状态
        document.getElementById('createWallet').disabled = false;
    });
}

function goBack() {
    // 恢复初始按钮布局
    document.getElementById('walletContainer').innerHTML = `
        <button id="createWallet" class="wallet-btn" onclick="createWallet()">创建钱包</button>
        <button id="importWallet" class="wallet-btn" onclick="importWallet()">导入钱包</button>
    `;
}

function importWallet() {
    // 显示导入钱包的输入界面
    document.getElementById('walletContainer').innerHTML = `
        <div id="importWalletForm">
            <textarea id="mnemonicInput" placeholder="请输入您的助记词" rows="4"></textarea>
            <button class="wallet-btn" onclick="submitMnemonic()">提交</button>
            <button class="wallet-btn" onclick="goBack()">返回</button>
        </div>
    `;
}

function submitMnemonic() {
    const mnemonic = document.getElementById('mnemonicInput').value.trim();
    if (mnemonic) {
        // 在此处添加导入钱包的逻辑
        alert('钱包导入成功！');
        // 可以在此显示钱包信息或跳转到钱包页面
        goBack();
    } else {
        alert('请输入有效的助记词！');
    }
}

function copyMnemonic(mnemonic) {
    navigator.clipboard.writeText(mnemonic).then(() => {
        alert('助记词已复制到剪贴板！');
    }).catch(err => {
        console.error('复制失败：', err);
    });
}
