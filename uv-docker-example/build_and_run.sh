#!/usr/bin/env sh

# 定义默认镜像名（可根据需求修改）
DEFAULT_IMAGE_NAME="fastapi-app"

# 获取用户输入的镜像名（第一个参数），无参数时使用默认值
IMAGE_NAME="${1:-$DEFAULT_IMAGE_NAME}"

# 检查Docker是否可用
if ! command -v docker &> /dev/null; then
    echo "错误：未检测到docker命令，请先安装Docker。"
    exit 1
fi

# 构建镜像（使用用户指定或默认的镜像名）
echo "开始构建镜像：${IMAGE_NAME}"
BUILD_OUTPUT=$(docker build -t "${IMAGE_NAME}" . 2>&1)
if [ $? -ne 0 ]; then
    echo "镜像构建失败："
    echo "${BUILD_OUTPUT}"
    exit 1
fi
echo "镜像构建成功：${IMAGE_NAME}"

# 设置交互式标志（与原脚本逻辑一致）
if [ -t 1 ]; then
    INTERACTIVE="-it"
else
    INTERACTIVE=""
fi

# 运行容器（使用构建的镜像名，保留原有卷、端口等参数）
echo "启动容器，使用镜像：${IMAGE_NAME}"
docker run \
    --rm \
    --volume .:/app \
    --volume /app/.venv \
    --publish 8000:8000 \
    ${INTERACTIVE} \
    "${IMAGE_NAME}" \
    "${@:2}"  # 仅传递第二个及之后的参数作为容器执行命令