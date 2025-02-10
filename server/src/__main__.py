import uvicorn
import enum
class LogLevel(str, enum.Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"

def main() -> None:
    uvicorn.run(
        "src.app.application:get_app",
        workers=2,
        host="127.0.0.1",
        port=8009,
        reload=True,
        reload_dirs=["/src/app"],
        log_level=LogLevel.INFO.value.lower(),
        factory= True
    )
    


if __name__ == "__main__":
    main()