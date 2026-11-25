package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.grad.alumni.common.PageResult;
import com.grad.alumni.common.R;
import com.grad.alumni.common.UserContext;
import com.grad.alumni.entity.SysMessage;
import com.grad.alumni.mapper.SysMessageMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

/** 站内消息：只返回当前登录人的消息，消息带业务编号与详情地址 */
@RestController
@RequestMapping("/api/message")
public class MessageController {

    private final SysMessageMapper mapper;

    public MessageController(SysMessageMapper mapper) { this.mapper = mapper; }

    @GetMapping("/page")
    public R<PageResult<SysMessage>> page(@RequestParam(defaultValue = "1") long page,
                                          @RequestParam(defaultValue = "10") long size) {
        Page<SysMessage> p = mapper.selectPage(new Page<>(page, size),
                new QueryWrapper<SysMessage>().eq("user_id", UserContext.userId()).orderByDesc("create_time"));
        return R.ok(PageResult.of(p));
    }

    @GetMapping("/unread")
    public R<Long> unread() {
        return R.ok(mapper.selectCount(new QueryWrapper<SysMessage>()
                .eq("user_id", UserContext.userId()).eq("read_flag", 0)));
    }

    @PostMapping("/{id}/read")
    public R<Void> read(@PathVariable Long id) {
        SysMessage m = new SysMessage();
        m.setId(id);
        m.setReadFlag(1);
        mapper.updateById(m);
        return R.ok();
    }

    @PostMapping("/read-all")
    public R<Void> readAll() {
        List<SysMessage> list = mapper.selectList(new QueryWrapper<SysMessage>()
                .eq("user_id", UserContext.userId()).eq("read_flag", 0));
        for (SysMessage m : list) {
            m.setReadFlag(1);
            mapper.updateById(m);
        }
        return R.ok();
    }

    /** 业务侧调用：写入站内消息并带上跳转地址 */
    public void push(Long userId, String title, String content, String type, String bizNo, String bizUrl) {
        SysMessage m = new SysMessage();
        m.setUserId(userId);
        m.setTitle(title);
        m.setContent(content);
        m.setMsgType(type);
        m.setBizNo(bizNo);
        m.setBizUrl(bizUrl);
        m.setReadFlag(0);
        m.setCreateTime(LocalDateTime.now());
        mapper.insert(m);
    }
}
