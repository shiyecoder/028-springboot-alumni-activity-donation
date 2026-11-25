package com.grad.alumni.common;

import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/** 全局异常处理：业务异常返回可直接展示的中文提示，其余统一兜底 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BizException.class)
    public R<Void> biz(BizException e) {
        return R.fail(e.getCode(), e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public R<Void> valid(MethodArgumentNotValidException e) {
        String msg = e.getBindingResult().getFieldErrors().stream()
                .findFirst().map(f -> f.getField() + " " + f.getDefaultMessage()).orElse("参数校验失败");
        return R.fail(400, msg);
    }

    @ExceptionHandler(Exception.class)
    public R<Void> other(Exception e) {
        e.printStackTrace();
        return R.fail(500, "系统繁忙：" + e.getMessage());
    }
}
