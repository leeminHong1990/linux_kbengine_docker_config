
- 需要修改 configurate.py 文件 的 192.168.1.52，修改成服务器本地地址；修改 download.py 192.168.1.11:8088 改成window 开发机地址

- 在 linux 上使用docker 配置 独立 kbengine服务

- 使用 docker-compose 工具配置

- 分布式 部署 应该使用相同的 UID

- 独立 部署 应该使用不同的 UID

- Docker 中的 root 用户 和 父节点 共享内核，UID 一致， 所以在Dockerfile中使用 新建用户 设置不同的UID 启动kbengine服务
