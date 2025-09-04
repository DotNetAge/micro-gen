#!/usr/bin/env python3
"""
微服务代码生成器命令行接口
"""

import os
import sys
import shutil
from pathlib import Path

import click
from loguru import logger

# 添加模板加载器
from micro_gen.core.templates.template_loader import TemplateLoader

def main():
    cli()


@click.group()
def cli():
    """微服务代码生成器命令行工具"""
    pass


@cli.command()
@click.argument("project_name")
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("./"),
    help="输出目录",
)
def init(project_name: str, output: Path):
    """初始化新的微服务项目 - 基于整洁架构和Go官方实践"""

    # 如果output就是当前目录且project_name就是当前目录名，直接使用当前目录
    if output.resolve() == Path.cwd().resolve():
        project_path = Path.cwd()
    else:
        project_path = output / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    # 创建目录结构
    directories = [
        "cmd/api",
        "data",
        "data/snapshots",
        "internal/entity",
        "internal/usecase",
        "adapter/handler",
        "adapter/repo",
        "pkg/config",
        "pkg/logger",
        "pkg/db",
        "pkg/http",
    ]

    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)

    # 初始化模板加载器
    template_loader = TemplateLoader(
        Path(__file__).parent / "core" / "templates" / "init"
    )

    # 使用模板渲染内容
    go_mod_content = template_loader.render_template(
        "go_mod.tmpl", {"project_name": project_name}
    )
    main_go_content = template_loader.render_template(
        "main.go.tmpl", {"project_name": project_name}
    )
    logger_content = template_loader.render_template(
        "logger.go.tmpl", {"project_name": project_name}
    )
    config_content = template_loader.render_template(
        "config.go.tmpl", {"project_name": project_name}
    )
    makefile_content = template_loader.render_template(
        "makefile.tmpl", {"project_name": project_name}
    )
    dockerfile_content = template_loader.render_template(
        "dockerfile.tmpl", {"project_name": project_name}
    )
    env_content = template_loader.render_template(
        "env.tmpl", {"project_name": project_name}
    )
    gitignore_content = template_loader.render_template(
        "gitignore.tmpl", {"project_name": project_name}
    )
    health_handler_content = template_loader.render_template(
        "health_handler.go.tmpl", {"project_name": project_name}
    )
    router_content = template_loader.render_template(
        "router.go.tmpl", {"project_name": project_name}
    )

    # 写入所有文件
    (project_path / "go.mod").write_text(go_mod_content)
    (project_path / "cmd" / "api" / "main.go").write_text(main_go_content)
    (project_path / "pkg" / "config" / "config.go").write_text(config_content)
    (project_path / "pkg" / "logger" / "logger.go").write_text(logger_content)
    (project_path / "adapter" / "handler" / "health_handler.go").write_text(
        health_handler_content
    )
    (project_path / "pkg" / "http" / "router.go").write_text(router_content)
    (project_path / "Makefile").write_text(makefile_content)
    (project_path / "Dockerfile").write_text(dockerfile_content)
    (project_path / ".env").write_text(env_content)
    (project_path / ".gitignore").write_text(gitignore_content)

    logger.success(f"✅ 项目 '{project_name}' 初始化完成！")
    logger.info(f"📁 项目路径: {project_path}")
    logger.info("🚀 下一步:")
    logger.info(f"  cd {project_name}")
    logger.info("  make deps    # 安装依赖")
    logger.info("  make run     # 运行服务")


@cli.command()
def validate():
    """验证配置文件格式"""
    config_file = Path("config.yaml")

    if not config_file.exists():
        logger.error("配置文件 config.yaml 不存在")
        return

    try:
        from .generator import MicroServiceGenerator

        generator = MicroServiceGenerator(config_path=config_file)
        generator.validate_config()
        logger.success("✅ 配置文件格式正确")
    except Exception as e:
        logger.error(f"❌ 配置文件验证失败: {e}")
        sys.exit(1)


@cli.command()
@click.option("--force", is_flag=True, help="强制覆盖现有文件")
def es(force: bool):
    """为现有项目添加ES事件机制 - 基于NATS JetStream"""

    # 使用当前目录作为项目路径
    project_path = Path.cwd()

    # 检查项目是否存在
    if not project_path.exists():
        logger.error(f"项目路径不存在: {project_path}")
        sys.exit(1)

    # 检查go.mod文件
    go_mod_file = project_path / "go.mod"
    if not go_mod_file.exists():
        logger.error("项目必须已初始化（需要go.mod文件）")
        sys.exit(1)

    try:
        # 读取项目名
        go_mod_content = go_mod_file.read_text()
        project_name = None
        for line in go_mod_content.split("\n"):
            if line.startswith("module "):
                project_name = line.replace("module ", "").strip()
                break

        if not project_name:
            logger.error("无法从go.mod中读取项目名")
            sys.exit(1)

        logger.info(f"🚀 为项目 '{project_name}' 添加ES事件机制...")

        # 初始化事件系统模板加载器
        from .core.templates.template_loader import TemplateLoader

        template_loader = TemplateLoader(
            Path(__file__).parent / "core" / "templates" / "es"
        )

        event_dirs = [
            "internal/entity",  # 领域事件接口
            "internal/usecase/event",  # 领域事件处理
            "pkg/event",  # 事件基础设施
        ]

        for directory in event_dirs:
            (project_path / directory).mkdir(parents=True, exist_ok=True)

        entity_event_content = template_loader.render_template(
            "entity_event.go.tmpl", {"project_name": project_name}
        )
        event_bus_content = template_loader.render_template(
            "event_bus.go.tmpl", {"project_name": project_name}
        )
        event_snapshot_content = template_loader.render_template(
            "event_snapshot.go.tmpl", {"project_name": project_name}
        )
        event_store_content = template_loader.render_template(
            "event_store.go.tmpl", {"project_name": project_name}
        )
        jetstream_store_content = template_loader.render_template(
            "jetstream_store.go.tmpl", {"project_name": project_name}
        )
        jetstream_bus_content = template_loader.render_template(
            "jetstream_bus.go.tmpl", {"project_name": project_name}
        )
        snapshot_store_content = template_loader.render_template(
            "snapshot_store.go.tmpl", {"project_name": project_name}
        )

        example_usage_content = template_loader.render_template(
            "example_usage.go.tmpl", {"project_name": project_name}
        )

        (project_path / "internal" / "entity" / "event.go").write_text(
            entity_event_content
        )
        (project_path / "internal" / "usecase" / "event" / "bus.go").write_text(
            event_bus_content
        )
        (project_path / "internal" / "usecase" / "event" / "snapshot.go").write_text(
            event_snapshot_content
        )
        (project_path / "internal" / "usecase" / "event" / "store.go").write_text(
            event_store_content
        )
        (project_path / "pkg" / "event" / "jetstream_store.go").write_text(
            jetstream_store_content
        )
        (project_path / "pkg" / "event" / "jetstream_bus.go").write_text(
            jetstream_bus_content
        )

        (project_path / "pkg" / "event" / "example_usage.go").write_text(
            example_usage_content
        )
        (project_path / "pkg" / "event" / "snapshot_store.go").write_text(
            snapshot_store_content
        )

        # 修改现有配置文件，添加事件系统配置
        _update_existing_config(project_path)

        logger.success("✅ ES事件机制添加完成！")
        logger.info("📁 文件已生成到相应目录")
        logger.info("🚀 下一步:")
        logger.info("  1. 安装依赖: go get github.com/nats-io/nats.go")
        logger.info("  2. 启动NATS: docker run -d -p 4222:4222 nats:latest")
        logger.info("  3. 使用pkg/event中的JetStream实现")
        logger.info("  4. 查看pkg/config/config.go了解新增配置选项")

    except Exception as e:
        logger.error(f"❌ 事件机制添加失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def _update_existing_config(project_path: Path):
    """智能修改现有配置文件，添加事件系统配置"""
    config_file = project_path / "pkg" / "config" / "config.go"

    if not config_file.exists():
        logger.warning("⚠️  配置文件不存在，跳过配置更新")
        return

    try:
        content = config_file.read_text()

        # 检查是否已存在事件配置
        if "NATSURL" in content and "StreamName" in content:
            logger.info("✅ 事件系统配置已存在，跳过更新")
            return

        # 1. 在Config结构体中添加事件配置
        struct_end = "\tLogLevel string\n}"
        new_struct_fields = """\tLogLevel string

	// 事件系统配置
	NATSURL     string
	StreamName  string
	ClusterName string"""

        if struct_end in content:
            content = content.replace(struct_end, new_struct_fields + "\n}")

        # 2. 在Load函数中添加默认值
        load_end = """		LogLevel:   getEnv("LOG_LEVEL", "info"),
	}

	return config, nil
}"""

        new_load_fields = """\t	LogLevel:   getEnv("LOG_LEVEL", "info"),
		NATSURL:    getEnv("NATS_URL", "nats://localhost:4222"),
		StreamName: getEnv("NATS_STREAM_NAME", "events"),
		ClusterName: getEnv("NATS_CLUSTER_NAME", "micro-services"),
	}

	return config, nil
}"""

        if load_end in content:
            content = content.replace(load_end, new_load_fields)
        else:
            # 尝试另一种格式匹配
            load_end_alt = """		LogLevel:   getEnv("LOG_LEVEL", "info"),
	}

	return config, nil
}"""
            new_load_fields_alt = """\t	LogLevel:   getEnv("LOG_LEVEL", "info"),
		NATSURL:    getEnv("NATS_URL", "nats://localhost:4222"),
		StreamName: getEnv("NATS_STREAM_NAME", "events"),
		ClusterName: getEnv("NATS_CLUSTER_NAME", "micro-services"),
	}

	return config, nil
}"""
            content = content.replace(load_end_alt, new_load_fields_alt)

        # 写回文件
        config_file.write_text(content)
        logger.success("✅ 事件系统配置已添加到 pkg/config/config.go")

    except Exception as e:
        logger.error(f"❌ 修改配置文件失败: {e}")
        logger.info("💡 请手动在 pkg/config/config.go 中添加以下配置:")
        logger.info("\tNATSURL     string")
        logger.info("\tStreamName  string")
        logger.info("\tClusterName string")
        logger.info("\t并在Load函数中设置默认值")


@cli.command()
def session():
    """为现有项目添加会话管理能力 - 基于Redis/Memory存储"""

    # 使用当前目录作为项目路径
    project_path = Path.cwd()

    # 检查项目是否存在
    if not project_path.exists():
        logger.error(f"项目路径不存在: {project_path}")
        sys.exit(1)

    # 检查go.mod文件
    go_mod_file = project_path / "go.mod"
    if not go_mod_file.exists():
        logger.error("项目必须已初始化（需要go.mod文件）")
        sys.exit(1)

    try:
        # 读取项目名
        go_mod_content = go_mod_file.read_text()
        project_name = None
        for line in go_mod_content.split("\n"):
            if line.startswith("module "):
                project_name = line.replace("module ", "").strip()
                break

        if not project_name:
            logger.error("无法从go.mod中读取项目名")
            sys.exit(1)

        logger.info(f"🚀 为项目 '{project_name}' 添加会话管理能力...")

        # 初始化会话管理模板加载器
        from .core.templates.template_loader import TemplateLoader

        template_loader = TemplateLoader(
            Path(__file__).parent / "core" / "templates" / "session"
        )

        session_dirs = [
            "internal/entity",  # 会话实体
            "internal/usecase/session",  # 会话用例
            "pkg/session",  # 会话基础设施
        ]

        for directory in session_dirs:
            (project_path / directory).mkdir(parents=True, exist_ok=True)

        entity_session_content = template_loader.render_template(
            "entity_session.go.tmpl", {"project_name": project_name}
        )
        usecase_session_content = template_loader.render_template(
            "usecase_session.go.tmpl", {"project_name": project_name}
        )
        redis_store_content = template_loader.render_template(
            "redis_store.go.tmpl", {"project_name": project_name}
        )
        memory_store_content = template_loader.render_template(
            "memory_store.go.tmpl", {"project_name": project_name}
        )
        badger_store_content = template_loader.render_template(
            "badger_store.go.tmpl", {"project_name": project_name}
        )
        session_manager_content = template_loader.render_template(
            "session_manager.go.tmpl", {"project_name": project_name}
        )
        # example_usage_content = template_loader.render_template(
        #     "example_usage.go.tmpl", {"project_name": project_name}
        # )

        (project_path / "internal" / "entity" / "session.go").write_text(
            entity_session_content
        )
        (project_path / "internal" / "usecase" / "session" / "service.go").write_text(
            usecase_session_content
        )
        (project_path / "pkg" / "session" / "redis_store.go").write_text(
            redis_store_content
        )
        (project_path / "pkg" / "session" / "memory_store.go").write_text(
            memory_store_content
        )
        (project_path / "pkg" / "session" / "badger_store.go").write_text(
            badger_store_content
        )
        (project_path / "pkg" / "session" / "session_manager.go").write_text(
            session_manager_content
        )
        # (project_path / "pkg" / "session" / "example_usage.go").write_text(
        #     example_usage_content
        # )

        # 修改现有配置文件，添加会话管理配置
        _update_session_config(project_path)

        logger.success("✅ 会话管理能力添加完成！")
        logger.info("📁 文件已生成到相应目录")
        logger.info("🚀 下一步:")
        logger.info("  1. 安装依赖:")
        logger.info("     go get github.com/redis/go-redis/v9")
        logger.info("     go get github.com/dgraph-io/badger/v4")
        logger.info("  2. 配置会话存储: 设置环境变量 SESSION_LEVEL=low|normal|high")
        logger.info("  3. 使用pkg/session中的SessionManager")
        # logger.info("  4. 查看pkg/session/example_usage.go了解使用方法")
        logger.info("  4. 存储策略选择:")
        logger.info("     - low (memory): 开发/测试环境，轻量级")
        logger.info("     - normal (badger): 中小型项目，本地持久化")
        logger.info("     - high (redis): 大型项目，高并发")

    except Exception as e:
        logger.error(f"❌ 会话管理添加失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def _update_session_config(project_path: Path):
    """智能修改现有配置文件，添加会话管理配置"""
    config_file = project_path / "pkg" / "config" / "config.go"

    if not config_file.exists():
        logger.warning("⚠️  配置文件不存在，跳过配置更新")
        return

    try:
        content = config_file.read_text()

        # 检查是否已存在会话相关配置
        has_session_config = "SessionStore" in content or "RedisAddr" in content

        # 1. 在Config结构体中添加配置
        struct_end = "\tLogLevel string\n}"
        new_struct_fields = """\tLogLevel string

	// 会话存储配置
	SessionLevel string // 会话存储级别: low (memory), normal (badger), high (redis)

	// Redis配置（用于redis存储）
	RedisAddr     string
	RedisPassword string
	RedisDB       int"""

        if struct_end in content and not has_session_config:
            content = content.replace(struct_end, new_struct_fields + "\n}")

        # 2. 在Load函数中添加默认值
        load_end = """\t\tLogLevel:   getEnv("LOG_LEVEL", "info"),
	}

\treturn config, nil
}"""

        new_load_fields = """\t\tLogLevel:      getEnv("LOG_LEVEL", "info"),
	\tSessionLevel:  getEnv("SESSION_LEVEL", "low"), // 可选: memory, badger, redis
	\tRedisAddr:     getEnv("REDIS_ADDR", "localhost:6379"),
	\tRedisPassword: getEnv("REDIS_PASSWORD", ""),
	\tRedisDB:       getEnvAsInt("REDIS_DB", 0),
	}

\treturn config, nil
}"""

        if load_end in content:
            content = content.replace(load_end, new_load_fields)

        # 写回文件
        config_file.write_text(content)
        logger.success("✅ 会话管理配置已添加到 pkg/config/config.go")

    except Exception as e:
        logger.error(f"❌ 修改配置文件失败: {e}")
        logger.info("💡 请手动在 pkg/config/config.go 中添加以下配置:")
        logger.info("\tSessionStore  string // memory, badger, redis")
        logger.info("\tRedisAddr     string")
        logger.info("\tRedisPassword string")
        logger.info("\tRedisDB       int")
        logger.info("\t并在Load函数中设置默认值")


@cli.command()
def saga():
    """为现有项目添加Saga分布式事务管理能力"""

    # 使用当前目录作为项目路径
    project_path = Path.cwd()

    # 检查项目是否存在
    if not project_path.exists():
        logger.error(f"项目路径不存在: {project_path}")
        sys.exit(1)

    # 检查go.mod文件
    go_mod_file = project_path / "go.mod"
    if not go_mod_file.exists():
        logger.error("项目必须已初始化（需要go.mod文件）")
        sys.exit(1)

    try:
        # 读取项目名
        go_mod_content = go_mod_file.read_text()
        project_name = None
        for line in go_mod_content.split("\n"):
            if line.startswith("module "):
                project_name = line.replace("module ", "").strip()
                break

        if not project_name:
            logger.error("无法从go.mod中读取项目名")
            sys.exit(1)

        logger.info(f"🚀 为项目 '{project_name}' 添加Saga分布式事务管理能力...")

        # 初始化Saga模板加载器
        from .core.templates.template_loader import TemplateLoader

        template_loader = TemplateLoader(
            Path(__file__).parent / "core" / "templates" / "saga"
        )

        saga_dirs = [
            "internal/entity",  # Saga实体
            "internal/usecase/saga",  # Saga用例
            "pkg/saga",  # Saga基础设施
        ]

        for directory in saga_dirs:
            (project_path / directory).mkdir(parents=True, exist_ok=True)

        entity_saga_content = template_loader.render_template(
            "entity_saga.go.tmpl", {"project_name": project_name}
        )
        usecase_saga_content = template_loader.render_template(
            "usecase_saga.go.tmpl", {"project_name": project_name}
        )
        saga_store_content = template_loader.render_template(
            "saga_store.go.tmpl", {"project_name": project_name}
        )
        saga_manager_content = template_loader.render_template(
            "saga_manager.go.tmpl", {"project_name": project_name}
        )
        example_usage_content = template_loader.render_template(
            "example_usage.go.tmpl", {"project_name": project_name}
        )

        (project_path / "internal" / "entity" / "saga.go").write_text(
            entity_saga_content
        )
        (project_path / "internal" / "usecase" / "saga" / "service.go").write_text(
            usecase_saga_content
        )
        (project_path / "pkg" / "saga" / "saga_store.go").write_text(saga_store_content)
        (project_path / "pkg" / "saga" / "saga_manager.go").write_text(
            saga_manager_content
        )
        (project_path / "pkg" / "saga" / "example_usage.go").write_text(
            example_usage_content
        )

        # 修改现有配置文件，添加Saga管理配置
        _update_saga_config(project_path)

        logger.success("✅ Saga分布式事务管理能力添加完成！")
        logger.info("📁 文件已生成到相应目录")
        logger.info("🚀 下一步:")
        logger.info("  1. 安装依赖:")
        logger.info("     go get github.com/redis/go-redis/v9")
        logger.info("     go get github.com/dgraph-io/badger/v4")
        logger.info("  2. 配置Saga存储: 设置环境变量 SAGA_LEVEL=low|normal|high")
        logger.info("  3. 使用pkg/saga中的SagaManager")
        logger.info("  4. 查看pkg/saga/example_usage.go了解使用方法")
        logger.info("  5. 存储策略选择:")
        logger.info("     - low (memory): 开发/测试环境，轻量级")
        logger.info("     - normal (badger): 中小型项目，本地持久化")
        logger.info("     - high (redis): 大型项目，高并发")

    except Exception as e:
        logger.error(f"❌ Saga管理添加失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def _update_saga_config(project_path: Path):
    """智能修改现有配置文件，添加Saga管理配置"""
    config_file = project_path / "pkg" / "config" / "config.go"

    if not config_file.exists():
        logger.warning("⚠️  配置文件不存在，跳过配置更新")
        return

    try:
        content = config_file.read_text()

        # 检查是否已存在Saga相关配置
        if "SagaLevel string" in content:
            logger.info("ℹ️  Saga配置已存在，跳过更新")
            return

        # 1. 在Config结构体中添加配置
        # 精确匹配SessionLevel的完整定义
        session_line = "\tSessionLevel string // 会话存储级别: low (memory), normal (badger), high (redis)"
        if session_line in content and "SagaLevel string" not in content:
            new_content = content.replace(
                session_line,
                f"{session_line}\n\n\t// Saga配置\n\tSagaLevel string // Saga存储级别: low (memory), normal (badger), high (redis)",
            )
            content = new_content
        elif "\tSessionLevel string" in content and "SagaLevel string" not in content:
            # 兼容旧的格式
            new_content = content.replace(
                "\tSessionLevel string",
                "\tSessionLevel string // 会话存储级别: low (memory), normal (badger), high (redis)\n\n\t// Saga配置\n\tSagaLevel string // Saga存储级别: low (memory), normal (badger), high (redis)",
            )
            content = new_content

        # 2. 在Load函数中添加默认值
        session_load_line = '\t\tSessionLevel:  getEnv("SESSION_LEVEL", "low"),'
        if session_load_line in content and "SagaLevel:" not in content:
            new_content = content.replace(
                session_load_line,
                f'{session_load_line}\n\t\tSagaLevel:     getEnv("SAGA_LEVEL", "low"), // 可选: low, normal, high',
            )
            content = new_content

        # 写回文件
        config_file.write_text(content)
        logger.success("✅ Saga管理配置已添加到 pkg/config/config.go")

    except Exception as e:
        logger.error(f"❌ 修改配置文件失败: {e}")
        logger.info("💡 请手动在 pkg/config/config.go 中添加以下配置:")
        logger.info("\tSagaLevel string // low, normal, high")


@cli.command()
def task():
    """为现有项目添加长时处理任务和定时任务管理能力"""

    # 使用当前目录作为项目路径
    project_path = Path.cwd()

    # 检查项目是否存在
    if not project_path.exists():
        logger.error(f"项目路径不存在: {project_path}")
        sys.exit(1)

    # 检查go.mod文件
    go_mod_file = project_path / "go.mod"
    if not go_mod_file.exists():
        logger.error("项目必须已初始化（需要go.mod文件）")
        sys.exit(1)

    try:
        # 读取项目名
        go_mod_content = go_mod_file.read_text()
        project_name = None
        for line in go_mod_content.split("\n"):
            if line.startswith("module "):
                project_name = line.replace("module ", "").strip()
                break

        if not project_name:
            logger.error("无法从go.mod中读取项目名")
            sys.exit(1)

        logger.info(f"🚀 为项目 '{project_name}' 添加长时处理任务和定时任务管理能力...")

        # 初始化任务管理模板加载器
        from .core.templates.template_loader import TemplateLoader

        template_loader = TemplateLoader(
            Path(__file__).parent / "core" / "templates" / "task"
        )

        task_dirs = [
            "internal/entity",  # 任务实体
            "internal/usecase/task",  # 任务用例
            "pkg/task",  # 任务基础设施
        ]

        for directory in task_dirs:
            (project_path / directory).mkdir(parents=True, exist_ok=True)

        entity_task_content = template_loader.render_template(
            "entity_task.go.tmpl", {"project_name": project_name}
        )
        usecase_task_content = template_loader.render_template(
            "usecase_task.go.tmpl", {"project_name": project_name}
        )
        task_store_content = template_loader.render_template(
            "task_store.go.tmpl", {"project_name": project_name}
        )
        redis_store_content = template_loader.render_template(
            "redis_store.go.tmpl", {"project_name": project_name}
        )
        badger_store_content = template_loader.render_template(
            "badger_store.go.tmpl", {"project_name": project_name}
        )
        task_manager_content = template_loader.render_template(
            "task_manager.go.tmpl", {"project_name": project_name}
        )
        example_usage_content = template_loader.render_template(
            "example_usage.go.tmpl", {"project_name": project_name}
        )

        (project_path / "internal" / "entity" / "task.go").write_text(
            entity_task_content
        )
        (project_path / "internal" / "usecase" / "task" / "service.go").write_text(
            usecase_task_content
        )
        (project_path / "pkg" / "task" / "task_store.go").write_text(task_store_content)
        (project_path / "pkg" / "task" / "redis_store.go").write_text(redis_store_content)
        (project_path / "pkg" / "task" / "badger_store.go").write_text(badger_store_content)
        (project_path / "pkg" / "task" / "task_manager.go").write_text(
            task_manager_content
        )
        (project_path / "pkg" / "task" / "example_usage.go").write_text(
            example_usage_content
        )

        # 修改现有配置文件，添加任务管理配置
        _update_task_config(project_path)

        logger.success("✅ 长时处理任务和定时任务管理能力添加完成！")
        logger.info("📁 文件已生成到相应目录")
        logger.info("🚀 下一步:")
        logger.info("  1. 安装依赖:")
        logger.info("     go get github.com/redis/go-redis/v9")
        logger.info("     go get github.com/dgraph-io/badger/v4")
        logger.info("     go get github.com/robfig/cron/v3")
        logger.info("  2. 配置任务存储: 设置环境变量 TASK_LEVEL=low|normal|high")
        logger.info("  3. 使用pkg/task中的TaskManager和TaskScheduler")
        logger.info("  4. 查看pkg/task/example_usage.go了解使用方法")
        logger.info("  5. 存储策略选择:")
        logger.info("     - low (memory): 开发/测试环境，轻量级")
        logger.info("     - normal (badger): 中小型项目，本地持久化")
        logger.info("     - high (redis): 大型项目，高并发")
        logger.info("  6. 定时任务特性:")
        logger.info("     - 支持CRON表达式")
        logger.info("     - 支持任务重试机制")
        logger.info("     - 支持任务优先级")
        logger.info("     - 支持任务超时控制")

    except Exception as e:
        logger.error(f"❌ 任务管理添加失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


def _update_task_config(project_path: Path):
    """智能修改现有配置文件，添加任务管理配置"""
    config_file = project_path / "pkg" / "config" / "config.go"

    if not config_file.exists():
        logger.warning("⚠️  配置文件不存在，跳过配置更新")
        return

    try:
        content = config_file.read_text()

        # 检查是否已存在任务相关配置
        if "TaskLevel string" in content:
            logger.info("ℹ️  任务配置已存在，跳过更新")
            return

        # 1. 在Config结构体中添加配置
        # 精确匹配SagaLevel的完整定义
        saga_line = "\tSagaLevel string // Saga存储级别: low (memory), normal (badger), high (redis)"
        if saga_line in content and "TaskLevel string" not in content:
            new_content = content.replace(
                saga_line,
                f"{saga_line}\n\n\t// 任务管理配置\n\tTaskLevel string // 任务存储级别: low (memory), normal (badger), high (redis)",
            )
            content = new_content
        elif "\tSagaLevel string" in content and "TaskLevel string" not in content:
            # 兼容旧的格式
            new_content = content.replace(
                "\tSagaLevel string",
                "\tSagaLevel string // Saga存储级别: low (memory), normal (badger), high (redis)\n\n\t// 任务管理配置\n\tTaskLevel string // 任务存储级别: low (memory), normal (badger), high (redis)",
            )
            content = new_content

        # 2. 在Load函数中添加默认值
        saga_load_line = '\t\tSagaLevel:     getEnv("SAGA_LEVEL", "low"),'
        if saga_load_line in content and "TaskLevel:" not in content:
            new_content = content.replace(
                saga_load_line,
                f'{saga_load_line}\n\t\tTaskLevel:     getEnv("TASK_LEVEL", "low"), // 可选: low, normal, high',
            )
            content = new_content

        # 写回文件
        config_file.write_text(content)
        logger.success("✅ 任务管理配置已添加到 pkg/config/config.go")

    except Exception as e:
        logger.error(f"❌ 修改配置文件失败: {e}")
        logger.info("💡 请手动在 pkg/config/config.go 中添加以下配置:")
        logger.info("\tTaskLevel string // low, normal, high")


@cli.command()
def projection():
    """为现有项目添加投影机制 - 基于CQRS模式的事件投影"""

    # 使用当前目录作为项目路径
    project_path = Path.cwd()

    # 检查项目是否存在
    if not project_path.exists():
        logger.error(f"项目路径不存在: {project_path}")
        sys.exit(1)

    # 检查go.mod文件
    go_mod_file = project_path / "go.mod"
    if not go_mod_file.exists():
        logger.error("项目必须已初始化（需要go.mod文件）")
        sys.exit(1)

    try:
        # 读取项目名
        go_mod_content = go_mod_file.read_text()
        project_name = None
        for line in go_mod_content.split("\n"):
            if line.startswith("module "):
                project_name = line.replace("module ", "").strip()
                break

        if not project_name:
            logger.error("无法从go.mod中读取项目名")
            sys.exit(1)

        logger.info(f"🚀 为项目 '{project_name}' 添加投影机制...")

        # 初始化投影模板加载器
        from .core.templates.template_loader import TemplateLoader

        template_loader = TemplateLoader(
            Path(__file__).parent / "core" / "templates" / "projection"
        )

        # 创建投影相关目录
        projection_dirs = [
            "internal/entity",  # 投影接口
            "internal/usecase/projection",  # 投影处理器
            "pkg/projection",  # 投影基础设施
        ]

        for directory in projection_dirs:
            (project_path / directory).mkdir(parents=True, exist_ok=True)

        # 渲染投影模板
        entity_projection_content = template_loader.render_template(
            "entity_projection.go.tmpl", {"project_name": project_name}
        )
        projection_store_content = template_loader.render_template(
            "projection_store.go.tmpl", {"project_name": project_name}
        )
        example_usage_content = template_loader.render_template(
            "example_usage.go.tmpl", {"project_name": project_name}
        )

        # 写入文件
        (project_path / "internal" / "entity" / "projection.go").write_text(
            entity_projection_content
        )
        (project_path / "pkg" / "projection" / "store.go").write_text(
            projection_store_content
        )
        (project_path / "pkg" / "projection" / "example_usage.go").write_text(
            example_usage_content
        )

        logger.success("✅ 投影机制文件已生成")

    except Exception as e:
        logger.error(f"❌ 添加投影机制失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
