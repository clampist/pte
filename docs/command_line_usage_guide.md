# PTE Framework 命令行使用指南

## 问题说明

在项目根目录执行 `pte all --parallel` 时出现 `zsh: command not found: pte` 错误，这是因为 `pte` 命令没有安装到系统 PATH 中。

## 原因分析

1. **PATH 环境变量**：Shell 会在 `$PATH` 环境变量中查找可执行命令
2. **本地脚本**：`pte` 脚本只在项目目录中可用，没有全局安装
3. **相对路径**：需要使用 `./pte` 来明确指定当前目录下的脚本

## 解决方案

### 方案1：使用安装脚本（推荐）

```bash
# 安装 pte 命令到系统 PATH
./install_pte.sh --install

# 重新加载 shell 配置
source ~/.zshrc

# 验证安装
pte help
```

### 方案2：手动安装

```bash
# 创建用户本地 bin 目录
mkdir -p ~/.local/bin

# 创建符号链接
ln -sf "$(pwd)/pte" ~/.local/bin/pte
ln -sf "$(pwd)/pte.sh" ~/.local/bin/pte.sh

# 添加到 PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 方案3：使用相对路径

```bash
# 在项目根目录使用相对路径
./pte all --parallel
./pte demo
./pte business
```

## 安装脚本功能

`install_pte.sh` 脚本提供以下功能：

```bash
# 安装 pte 命令
./install_pte.sh --install

# 卸载 pte 命令
./install_pte.sh --uninstall

# 查看安装状态
./install_pte.sh --status

# 显示帮助信息
./install_pte.sh --help
```

## 验证安装

安装完成后，可以通过以下方式验证：

```bash
# 检查 pte 命令是否可用
which pte

# 测试 pte 命令
pte help

# 运行测试
pte all --parallel
```

## 常见问题

### Q: 安装后仍然提示 "command not found"
A: 请重新加载 shell 配置：
```bash
source ~/.zshrc
# 或者重新打开终端
```

### Q: 如何卸载 pte 命令？
A: 使用卸载命令：
```bash
./install_pte.sh --uninstall
source ~/.zshrc
```

### Q: 可以在其他目录使用 pte 命令吗？
A: 安装到 PATH 后，可以在任何目录使用 `pte` 命令。

## 命令使用示例

```bash
# 运行所有测试（并行）
pte all --parallel

# 运行 Demo 测试
pte demo

# 运行业务测试
pte business

# 运行指定路径的测试
pte run test/department/user

# 运行特定测试文件
pte run test/department/user/demo_framework_structure.py

# 运行数据库测试
pte db-test

# 验证 MySQL 环境
pte mysql-verify
```

## 注意事项

1. **Python 环境**：确保已激活正确的 Python 环境（pyenv activate pte）
2. **依赖安装**：确保已安装所有必要的依赖包
3. **权限问题**：如果遇到权限问题，可能需要使用 `sudo` 安装到系统目录
4. **Shell 配置**：安装后需要重新加载 shell 配置或重启终端

## 技术细节

- **安装位置**：`~/.local/bin/`（用户本地目录）
- **符号链接**：创建 `pte` 和 `pte.sh` 的符号链接
- **PATH 配置**：自动添加到 `~/.zshrc` 或 `~/.bashrc`
- **兼容性**：支持 zsh 和 bash shell
