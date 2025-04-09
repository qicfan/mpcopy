# mpcopy
## 将MP整理完的文件复制到其他目录（可以是CD2挂在的网盘目录，达到实时同步到网盘的目的）
## 需要配合supervisor或者其他任务管理工具使用，程序本身不会后台运行
## docker没有测试过,b不保证可以正常使用

### 一、直接执行
python main.py --src_path="SRC_PATH" --dest_path="DEST_PATH"

### 二、DOCKER
```bash
docker run -d \
    --name mpcopy \
    -e "TZ=Asia/Shanghai" \
    -v /vol1/1000/docker/mpcopy/logs:/app/logs \
    -v /vol1/1000/docker/clouddrive2/shared/115/Media:/dest \
    -v /vol3/1000/Media:/src \
    --restart unless-stopped \
    qicfan/mpcopy:latest
```

或者compose

```
services:
  mpcopy:
    image: qicfan/mpcopy
    container_name: mpcopy
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - /vol1/1000/docker/mpcopy/logs:/app/logs # 运行日志和数据
      - /vol1/1000/docker/clouddrive2/shared/115/Media:/dest # 目标目录（CD2挂载的115） 
      - /vol3/1000/Media:/src # 需要监控的源目录
    restart: unless-stopped
```

#### Docker 配置解释
- `-v /vol1/1000/docker/mpcopy/logs:/app/logs`: 程序运行时的日志目录
- `-v /vol1/1000/docker/clouddrive2/shared/115/Media:/dest`: CD2挂载的115下的目录，会将文件复制到这里达到上传到115的目的。
- `-v /vol3/1000/Media:/src` 需要监控的目录，一般是MP整理的目录