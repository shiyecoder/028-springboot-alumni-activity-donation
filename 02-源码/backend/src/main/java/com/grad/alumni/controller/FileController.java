package com.grad.alumni.controller;

import com.grad.alumni.common.BizException;
import com.grad.alumni.common.R;
import com.grad.alumni.common.UserContext;
import com.grad.alumni.entity.SysFile;
import com.grad.alumni.mapper.SysFileMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

/** 文件上传：保存到项目根目录 uploads/yyyyMM/，数据库只存相对路径 */
@RestController
@RequestMapping("/api/file")
public class FileController {

    private static final Set<String> ALLOWED = Set.of("jpg", "jpeg", "png", "webp", "gif", "pdf");

    @Value("${app.upload-dir:./uploads}")
    private String uploadDir;

    private final SysFileMapper fileMapper;

    public FileController(SysFileMapper fileMapper) { this.fileMapper = fileMapper; }

    @PostMapping("/upload")
    public R<Map<String, Object>> upload(@RequestParam("file") MultipartFile file,
                                         @RequestParam(required = false, defaultValue = "COMMON") String bizType) {
        if (file == null || file.isEmpty()) throw new BizException("请选择要上传的文件");
        String origin = file.getOriginalFilename() == null ? "file" : file.getOriginalFilename();
        String ext = origin.contains(".") ? origin.substring(origin.lastIndexOf('.') + 1).toLowerCase() : "";
        if (!ALLOWED.contains(ext)) throw new BizException("不支持的文件类型：" + ext);
        if (file.getSize() > 20 * 1024 * 1024) throw new BizException("文件不能超过 20MB");
        String month = LocalDate.now().toString().substring(0, 7).replace("-", "");
        String name = UUID.randomUUID().toString().replace("-", "") + "." + ext;
        try {
            Path dir = Paths.get(uploadDir, month).toAbsolutePath().normalize();
            Files.createDirectories(dir);
            file.transferTo(dir.resolve(name).toFile());
        } catch (IOException e) {
            throw new BizException("文件保存失败：" + e.getMessage());
        }
        String rel = "/uploads/" + month + "/" + name;
        SysFile sf = new SysFile();
        sf.setFileName(origin);
        sf.setFilePath(rel);
        sf.setFileSize(file.getSize());
        sf.setFileType(file.getContentType());
        sf.setBizType(bizType);
        sf.setUploaderId(UserContext.userId());
        sf.setUploaderName(UserContext.name());
        sf.setCreateTime(LocalDateTime.now());
        fileMapper.insert(sf);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("path", rel);
        out.put("name", origin);
        out.put("size", file.getSize());
        return R.ok(out);
    }
}
