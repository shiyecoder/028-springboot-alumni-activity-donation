package com.grad.alumni.common;

/** 业务异常：由全局异常处理器转成统一 JSON，前端直接展示 msg */
public class BizException extends RuntimeException {
    private final int code;

    public BizException(String msg) {
        super(msg);
        this.code = 500;
    }

    public BizException(int code, String msg) {
        super(msg);
        this.code = code;
    }

    public int getCode() { return code; }
}
