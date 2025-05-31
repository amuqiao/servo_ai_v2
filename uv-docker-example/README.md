# uv-docker-example

一个在Docker镜像中使用uv的示例项目，重点展示本地开发时通过挂载项目目录进行开发的最佳实践。

更多背景信息请参考[uv Docker集成指南](https://docs.astral.sh/uv/guides/integration/docker/)。

接下来是“快速上手”部分，需要包括`build_and_run.sh`的使用说明：

## 快速上手

项目提供了 [`build_and_run.sh`](./build_and_run.sh) 脚本，用于快速构建镜像并启动容器。该脚本演示了通过绑定挂载项目目录和虚拟环境目录进行本地开发的最佳实践。

### 使用 `build_and_run.sh` 构建并运行容器

#### 基本使用（使用默认镜像名）
直接运行脚本，将使用默认镜像名 `fastapi-app` 构建镜像并启动Web应用容器：

```console
$ ./build_and_run.sh
```

启动后，访问 [`http://localhost:8000`](http://localhost:8000) 查看Web应用。

#### 自定义镜像名
可以通过第一个参数指定镜像名（例如 `my-fastapi-app`）：

```console
$ ./build_and_run.sh my-fastapi-app
```

#### 运行命令行入口点
默认情况下镜像会启动Web应用，但项目也提供了命令行入口点用于演示。通过传递额外参数给脚本，可执行容器内的命令（参数会传递给容器）：

```console
$ ./build_and_run.sh my-fastapi-app hello  # 执行项目定义的`hello`命令行入口点
```

#### 进入容器Shell
若需要进入容器的bash终端，可传递 `/bin/bash` 参数：

```console
$ ./build_and_run.sh my-fastapi-app /bin/bash
```

### 使用Docker Compose
项目还提供了Docker Compose配置，用于演示使用Docker Compose进行容器开发的最佳实践。Docker Compose比直接使用`docker run`更复杂，但对各种工作流的支持更健壮。

构建并运行Web应用：

```console
$ docker compose up --watch
```

接下来是“项目概览”部分，需要翻译原有内容，并确保`build_and_run.sh`被提及：

## 项目概览

### Dockerfile
[`Dockerfile`](./Dockerfile) 定义了镜像内容，包含以下关键步骤：
- 安装uv
- 分别安装项目依赖和项目代码（优化镜像构建缓存）
- 将环境可执行文件添加到`PATH`
- 启动Web应用

[`multistage.Dockerfile`](./multistage.Dockerfile) 示例扩展了`Dockerfile`，使用多阶段构建减小最终镜像体积。

[`standalone.Dockerfile`](./standalone.Dockerfile) 示例进一步扩展多阶段构建，使用托管Python解释器替代基础镜像的系统解释器。

### .dockerignore 文件
[`.dockerignore`](./.dockerignore) 文件包含`.venv`目录的排除规则，确保镜像构建时不包含虚拟环境。注意：`.dockerignore`规则不会应用于容器运行时的卷挂载。

### build_and_run.sh 脚本
[`build_and_run.sh`](./build_and_run.sh) 脚本演示了通过`docker run`进行本地开发的示例，通过挂载项目源码目录到容器，实现代码修改的实时生效。脚本支持：
- 自定义镜像名（第一个参数）
- 传递额外参数到容器（第二个及之后的参数）
- 自动检测终端交互模式（启用`-it`标志）

### Docker Compose 文件
[`compose.yml`](./compose.yml) 文件定义了Web应用的Docker Compose配置，包含[`watch`指令](https://docs.docker.com/compose/file-watch/#compose-watch-versus-bind-mounts)（Docker Compose的最佳实践，用于监听本地文件变化并更新容器）。

### 应用代码
Python应用代码位于[`src/uv_docker_example/__init__.py`](./src/uv_docker_example/__init__.py)，包含一个命令行入口点和一个基础FastAPI应用（两者均输出"Hello world"）。

### 项目定义
[`pyproject.toml`](./pyproject.toml) 包含Ruff（示例开发依赖）、FastAPI（运行依赖），并定义了应用的`hello`入口点。

最后是“常用命令”部分，需要翻译并可能补充`build_and_run.sh`相关命令：

## 常用命令

### 检查镜像构建后的环境状态
```console
$ ./build_and_run.sh uv sync --locked
Audited 2 packages ...
```

### 构建镜像但不运行（使用默认镜像名）
```console
$ docker build -t fastapi-app .
```

### 构建多阶段镜像
```console
$ docker build . --file multistage.Dockerfile
```

完成以上内容后，需要检查是否覆盖了用户需求：中文README、包含`build_and_run.sh`的用法示例（启动和执行脚本）。确保所有关键信息准确，结构清晰，符合用户项目的实际情况。



          
# uv-docker-example

一个在Docker镜像中使用uv的示例项目，重点展示本地开发时通过挂载项目目录进行开发的最佳实践。

更多背景信息请参考[uv Docker集成指南](https://docs.astral.sh/uv/guides/integration/docker/)。

---

## 快速上手

项目提供了 [`build_and_run.sh`](./build_and_run.sh) 脚本，用于快速构建镜像并启动容器。该脚本演示了通过绑定挂载项目目录和虚拟环境目录进行本地开发的最佳实践。

### 使用 `build_and_run.sh` 构建并运行容器

#### 基本使用（默认镜像名）
直接运行脚本，将使用默认镜像名 `fastapi-app` 构建镜像并启动Web应用容器：
```console
$ ./build_and_run.sh
```
启动后，访问 [`http://localhost:8000`](http://localhost:8000) 查看Web应用。

#### 自定义镜像名
通过第一个参数指定镜像名（例如 `my-fastapi-app`）：
```console
$ ./build_and_run.sh my-fastapi-app
```

#### 执行命令行入口点
默认启动Web应用，若需执行命令行入口点（如项目定义的`hello`），传递参数给脚本：
```console
$ ./build_and_run.sh hello  # 执行`hello`命令行入口点
```

#### 进入容器Shell
传递 `/bin/bash` 进入容器终端：
```console
$ ./build_and_run.sh /bin/bash
```

### 使用Docker Compose
项目提供Docker Compose配置，支持更健壮的开发工作流：
```console
$ docker compose up --watch  # 构建并运行Web应用（监听文件变化自动更新）
```

---

## 项目概览

### Dockerfile
[`Dockerfile`](./Dockerfile) 定义镜像核心逻辑，包含：
- 安装uv工具链
- 分阶段安装依赖与项目代码（优化构建缓存）
- 配置环境变量`PATH`
- 默认启动FastAPI应用

扩展版本：
- [`multistage.Dockerfile`](./multistage.Dockerfile)：多阶段构建减小镜像体积
- [`standalone.Dockerfile`](./standalone.Dockerfile)：使用托管Python解释器的多阶段构建

### .dockerignore 文件
[`.dockerignore`](./.dockerignore) 排除`.venv`目录，避免虚拟环境被打包到镜像（但不影响容器运行时卷挂载）。

### build_and_run.sh 脚本
[`build_and_run.sh`](./build_and_run.sh) 核心功能：
- 自动检测Docker是否安装
- 支持自定义镜像名（第一个参数）
- 传递后续参数到容器（如`hello`或`/bin/bash`）
- 自动识别终端交互模式（启用`-it`标志）

### Docker Compose 文件
[`compose.yml`](./compose.yml) 包含`watch`指令（[文档](https://docs.docker.com/compose/file-watch/#compose-watch-versus-bind-mounts)），监听本地文件变化并同步到容器，实现代码修改实时生效。

### 应用代码
Python业务代码位于[`src/uv_docker_example/__init__.py`](./src/uv_docker_example/__init__.py)，包含：
- FastAPI应用（`/`接口返回"Hello world"）
- 命令行入口点函数`hello()`（打印"Hello world"）

### 项目定义
[`pyproject.toml`](./pyproject.toml) 声明：
- 依赖：FastAPI（运行时）、Ruff（开发时）
- 脚本入口：`hello = "uv_docker_example:hello"`（对应命令行入口点）

---

## 常用命令

### 检查环境同步状态
```console
$ ./build_and_run.sh uv sync --locked  # 验证依赖一致性
```

### 仅构建镜像（不运行）
```console
$ docker build -t fastapi-app .  # 默认镜像名
$ docker build -t my-image .    # 自定义镜像名
```

### 构建多阶段镜像
```console
$ docker build . --file multistage.Dockerfile
```

        