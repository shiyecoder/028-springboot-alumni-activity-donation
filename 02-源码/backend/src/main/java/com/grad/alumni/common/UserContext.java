package com.grad.alumni.common;

/** 当前登录人上下文（ThreadLocal）：角色 + 数据范围 SELF / ORG / ALL */
public class UserContext {

    public record LoginUser(Long id, String name, String roleCode, Long orgId, String dataScope) {
    }

    private static final ThreadLocal<LoginUser> HOLDER = new ThreadLocal<>();

    public static void set(LoginUser u) { HOLDER.set(u); }

    public static LoginUser get() { return HOLDER.get(); }

    public static Long userId() {
        LoginUser u = HOLDER.get();
        return u == null ? null : u.id();
    }

    public static String name() {
        LoginUser u = HOLDER.get();
        return u == null ? "系统" : u.name();
    }

    public static String role() {
        LoginUser u = HOLDER.get();
        return u == null ? "" : u.roleCode();
    }

    public static Long orgId() {
        LoginUser u = HOLDER.get();
        return u == null ? null : u.orgId();
    }

    public static boolean isAlumni() { return "ALUMNI".equals(role()); }
    public static boolean isLiaison() { return "LIAISON".equals(role()); }
    public static boolean isAdmin() { return "ADMIN".equals(role()); }
    public static boolean isFinance() { return "FINANCE".equals(role()); }

    public static void clear() { HOLDER.remove(); }
}
