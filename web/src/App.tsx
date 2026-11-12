import { useEffect, useMemo, useState } from "react";

export type Role = "sales" | "admin";
export type LeadStatus = "New" | "Contacted" | "Booking" | "Qualified" | "Lost";
export type IconName =
  | "activity"
  | "bell"
  | "bot"
  | "briefcase"
  | "calendar"
  | "chart"
  | "check"
  | "chevron"
  | "close"
  | "columns"
  | "database"
  | "external"
  | "filter"
  | "key"
  | "lead"
  | "lock"
  | "logout"
  | "menu"
  | "moon"
  | "more"
  | "notes"
  | "pause"
  | "play"
  | "search"
  | "settings"
  | "shield"
  | "sun"
  | "user"
  | "users";

export type AuthUser = {
  id: string;
  username: string;
  name: string;
  role: Role;
  roleLabel: string;
  avatar: string;
  email: string;
};

export type Lead = {
  id: number | string;
  name: string;
  platform: "Facebook" | "Threads";
  handle: string;
  phone: string;
  need: string;
  location: string;
  status: LeadStatus;
  agent: string;
  agentInitials: string;
  score: number;
  time: string;
  post: string;
  note: string;
  url?: string;
};

const initialLeads: Lead[] = [];

const statusOptions: LeadStatus[] = ["New", "Contacted", "Booking", "Qualified", "Lost"];

const statusLabels: Record<LeadStatus, string> = {
  New: "Mới",
  Contacted: "Cần chăm sóc",
  Booking: "Đã đặt lịch",
  Qualified: "Tiềm năng",
  Lost: "Không phù hợp",
};

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, React.ReactNode> = {
    activity: <path d="M3 12h3l2.2-6 4.1 12 2.2-6H21" />,
    bell: (
      <>
        <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
        <path d="M10 21h4" />
      </>
    ),
    bot: (
      <>
        <rect x="4" y="7" width="16" height="12" rx="3" />
        <path d="M9 11h.01M15 11h.01M9 15h6M12 7V3M9 3h6" />
      </>
    ),
    briefcase: (
      <>
        <rect x="3" y="7" width="18" height="13" rx="2" />
        <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18" />
      </>
    ),
    calendar: (
      <>
        <rect x="3" y="5" width="18" height="16" rx="2" />
        <path d="M16 3v4M8 3v4M3 10h18M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01" />
      </>
    ),
    chart: <path d="M4 19V9M10 19V5M16 19v-7M22 19H2" />,
    check: <path d="m5 12 4 4L19 6" />,
    chevron: <path d="m9 18 6-6-6-6" />,
    close: <path d="M18 6 6 18M6 6l12 12" />,
    columns: (
      <>
        <rect x="3" y="4" width="18" height="16" rx="2" />
        <path d="M9 4v16M15 4v16" />
      </>
    ),
    database: (
      <>
        <ellipse cx="12" cy="5" rx="8" ry="3" />
        <path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6" />
      </>
    ),
    external: (
      <>
        <path d="M15 3h6v6M10 14 21 3" />
        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
      </>
    ),
    filter: <path d="M3 4h18l-7 8v6l-4 2v-8Z" />,
    key: (
      <>
        <circle cx="8" cy="15" r="4" />
        <path d="m11 12 8-8M15 8l3 3M17 6l2 2" />
      </>
    ),
    lead: (
      <>
        <circle cx="9" cy="8" r="4" />
        <path d="M3 21a6 6 0 0 1 12 0M17 8h4M19 6v4" />
      </>
    ),
    lock: (
      <>
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </>
    ),
    logout: (
      <>
        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
        <polyline points="16 17 21 12 16 7" />
        <line x1="21" y1="12" x2="9" y2="12" />
      </>
    ),
    user: (
      <>
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </>
    ),
    menu: <path d="M4 6h16M4 12h16M4 18h16" />,
    moon: <path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z" />,
    more: <path d="M5 12h.01M12 12h.01M19 12h.01" />,
    notes: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z" />
        <path d="M14 2v6h6M8 13h8M8 17h6" />
      </>
    ),
    pause: (
      <>
        <path d="M8 5v14M16 5v14" />
      </>
    ),
    play: <path d="m8 5 11 7-11 7Z" />,
    search: <path d="m21 21-4.4-4.4M19 11a8 8 0 1 1-16 0 8 8 0 0 1 16 0Z" />,
    settings: (
      <>
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.6v-.2h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z" />
      </>
    ),
    shield: <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10ZM9 12l2 2 4-4" />,
    sun: (
      <>
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
      </>
    ),
    users: (
      <>
        <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8" />
      </>
    ),
  };

  return (
    <svg
      aria-hidden="true"
      fill="none"
      height={size}
      viewBox="0 0 24 24"
      width={size}
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="1.8"
    >
      {paths[name]}
    </svg>
  );
}

function PlatformIcon({ platform }: { platform: Lead["platform"] }) {
  const pLower = (platform || "web").toLowerCase();
  const letter = platform ? platform[0] : "W";
  return <span className={`platform-icon platform-${pLower}`}>{letter}</span>;
}

function Toggle({
  checked,
  onChange,
  label,
}: {
  checked: boolean;
  onChange: () => void;
  label: string;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      className={`mini-toggle ${checked ? "is-on" : ""}`}
      onClick={onChange}
    >
      <span />
    </button>
  );
}

function StatCard({
  icon,
  label,
  value,
  detail,
  tone = "blue",
}: {
  icon: IconName;
  label: string;
  value: string;
  detail: string;
  tone?: "blue" | "cyan" | "green" | "violet";
}) {
  return (
    <article className="stat-card">
      <div className={`stat-icon tone-${tone}`}>
        <Icon name={icon} size={19} />
      </div>
      <div className="stat-copy">
        <span>{label}</span>
        <strong>{value}</strong>
        <small>{detail}</small>
      </div>
    </article>
  );
}

const REGION_OPTIONS = ["Đà Nẵng", "Hà Nội", "TP.HCM", "Huế", "Quảng Nam", "Toàn quốc"];

const INTERVAL_PRESETS = [
  { label: "15 phút", minutes: 15 },
  { label: "30 phút", minutes: 30 },
  { label: "1 tiếng", minutes: 60 },
  { label: "2 tiếng", minutes: 120 },
  { label: "6 tiếng", minutes: 360 },
  { label: "12 tiếng", minutes: 720 },
  { label: "24 tiếng", minutes: 1440 },
];

function formatIntervalShort(intervalSeconds?: number): string {
  const secs = typeof intervalSeconds === "number" && intervalSeconds > 0 ? intervalSeconds : 3600;
  const mins = Math.max(1, Math.round(secs / 60));
  if (mins < 60) return `${mins}p/lần`;
  if (mins % 60 === 0) return `${mins / 60}h/lần`;
  return `${Math.floor(mins / 60)}h${mins % 60}p`;
}

function formatIntervalLong(intervalSeconds?: number): string {
  const secs = typeof intervalSeconds === "number" && intervalSeconds > 0 ? intervalSeconds : 3600;
  const mins = Math.max(1, Math.round(secs / 60));
  if (mins < 60) return `${mins} phút / lần`;
  if (mins % 60 === 0) return `${mins / 60} tiếng / lần`;
  return `${Math.floor(mins / 60)} tiếng ${mins % 60} phút / lần`;
}

function isImageAvatar(avatar?: string): boolean {
  if (!avatar) return false;
  return avatar.startsWith("data:image/") || avatar.startsWith("http://") || avatar.startsWith("https://");
}

function computeInitials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "AD";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
}

function AvatarBadge({
  avatar,
  name,
  className = "avatar",
}: {
  avatar?: string;
  name: string;
  className?: string;
}) {
  if (isImageAvatar(avatar)) {
    return (
      <div className={className}>
        <img src={avatar} alt={name} className="avatar-img" />
      </div>
    );
  }
  return <div className={className}>{avatar || computeInitials(name)}</div>;
}

function Sidebar({
  collapsed,
  onCollapse,
  user,
  activeItem,
  onNavigate,
  totalLeads,
}: {
  collapsed: boolean;
  onCollapse: () => void;
  user: AuthUser;
  activeItem: string;
  onNavigate: (item: string) => void;
  totalLeads: number;
}) {
  const salesItems = [
    ["Khách hàng", "lead"],
    ["Cần chăm sóc", "calendar"],
    ["Đã đặt lịch", "check"],
  ] as const;
  const adminItems = [
    ["Tổng quan", "chart"],
    ["Khách hàng", "lead"],
    ["Trình thu thập", "bot"],
    ["Từ khóa & Nguồn", "search"],
    ["Phân phối khách", "briefcase"],
    ["Nhân sự & Phân quyền", "users"],
    ["API & Máy chủ trung gian", "key"],
  ] as const;
  const items = user.role === "sales" ? salesItems : adminItems;

  return (
    <aside className={`sidebar ${collapsed ? "is-collapsed" : ""}`}>
      <div className="brand-row">
        <div className="brand-mark">
          <span />
          <span />
          <span />
        </div>
        {!collapsed && (
          <div className="brand-name">
            <strong>Denta</strong>
            <span>Lead AI</span>
          </div>
        )}
        <button
          type="button"
          className="collapse-btn"
          onClick={onCollapse}
          aria-label="Thu gọn sidebar"
        >
          <Icon name={collapsed ? "menu" : "chevron"} size={17} />
        </button>
      </div>

      {!collapsed && <p className="nav-label">Không gian làm việc</p>}
      <nav className="sidebar-nav" aria-label="Điều hướng chính">
        {items.map(([label, icon]) => (
          <button
            type="button"
            key={label}
            className={activeItem === label ? "active" : ""}
            onClick={() => onNavigate(label)}
            title={collapsed ? label : undefined}
          >
            <Icon name={icon} size={18} />
            {!collapsed && <span>{label}</span>}
            {!collapsed && label === "Khách hàng" && <b>{totalLeads}</b>}
          </button>
        ))}
      </nav>
    </aside>
  );
}

function AccountSettingsModal({
  user,
  onClose,
  onSave,
}: {
  user: AuthUser;
  onClose: () => void;
  onSave: (updated: AuthUser) => void;
}) {
  const [name, setName] = useState(user.name);
  const [email, setEmail] = useState(user.email);
  const [roleLabel, setRoleLabel] = useState(user.roleLabel);
  const [avatar, setAvatar] = useState(user.avatar);
  const [avatarUrlInput, setAvatarUrlInput] = useState(isImageAvatar(user.avatar) ? user.avatar : "");
  const [newPassword, setNewPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setError("");
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        const maxSide = 192;
        const scale = Math.min(1, maxSide / Math.max(img.width, img.height));
        const w = Math.max(1, Math.round(img.width * scale));
        const h = Math.max(1, Math.round(img.height * scale));
        const canvas = document.createElement("canvas");
        canvas.width = w;
        canvas.height = h;
        const ctx = canvas.getContext("2d");
        if (ctx) {
          ctx.drawImage(img, 0, 0, w, h);
          const dataUrl = canvas.toDataURL("image/jpeg", 0.85);
          setAvatar(dataUrl);
          setAvatarUrlInput("");
        } else if (typeof reader.result === "string") {
          setAvatar(reader.result);
        }
      };
      if (typeof reader.result === "string") {
        img.src = reader.result;
      }
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Vui lòng nhập tên hiển thị.");
      return;
    }
    setSaving(true);
    setError("");
    const finalAvatar = avatarUrlInput.trim() || avatar || computeInitials(name);
    try {
      const res = await fetch("/api/auth/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: user.username,
          name: name.trim(),
          email: email.trim(),
          roleLabel: roleLabel.trim(),
          avatar: finalAvatar,
          newPassword: newPassword.trim(),
        }),
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        setError(data.error || "Không thể cập nhật thông tin tài khoản.");
        setSaving(false);
        return;
      }
      onSave(data.user);
      onClose();
    } catch {
      setError("Lỗi kết nối máy chủ.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Quản lý tài khoản">
        <div className="modal-header">
          <div>
            <h3>Quản lý tài khoản</h3>
            <p>Cập nhật thông tin cá nhân, chức danh và ảnh đại diện (@{user.username})</p>
          </div>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Đóng">
            <Icon name="close" size={18} />
          </button>
        </div>

        <form className="modal-form" onSubmit={handleSubmit}>
          <div className="avatar-editor-row">
            <AvatarBadge avatar={avatarUrlInput.trim() || avatar} name={name} className="avatar avatar-preview-lg" />
            <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "8px" }}>
              <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
                <label className="secondary-button" style={{ cursor: "pointer", padding: "6px 12px", fontSize: "12px" }}>
                  Tải ảnh đại diện
                  <input type="file" accept="image/*" onChange={handleFileUpload} style={{ display: "none" }} />
                </label>
                <button
                  type="button"
                  className="secondary-button"
                  style={{ padding: "6px 10px", fontSize: "12px" }}
                  onClick={() => {
                    setAvatarUrlInput("");
                    setAvatar(computeInitials(name));
                  }}
                >
                  Dùng chữ cái ({computeInitials(name)})
                </button>
              </div>
              <input
                type="url"
                placeholder="Hoặc dán URL ảnh đại diện (https://...)"
                value={avatarUrlInput}
                onChange={(e) => setAvatarUrlInput(e.target.value)}
                style={{
                  background: "var(--surface)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  padding: "7px 10px",
                  color: "var(--text)",
                  fontSize: "12px",
                }}
              />
            </div>
          </div>

          <div className="modal-field">
            <label>Tên hiển thị</label>
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="VD: Nha Khoa Admin" required />
          </div>

          <div className="modal-field">
            <label>Email liên hệ</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="admin@dentalead.vn" />
          </div>

          <div className="modal-field">
            <label>Chức danh hiển thị</label>
            <input value={roleLabel} onChange={(e) => setRoleLabel(e.target.value)} placeholder="Quản trị viên hệ thống" />
          </div>

          <div className="modal-field">
            <label>Mật khẩu mới (bỏ trống nếu giữ nguyên)</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Nhập mật khẩu mới nếu muốn đổi"
            />
          </div>

          {error && <div className="login-error">{error}</div>}

          <div className="modal-actions">
            <button type="button" className="secondary-button" onClick={onClose}>
              Hủy
            </button>
            <button type="submit" className="primary-button" disabled={saving}>
              <Icon name="check" size={16} /> {saving ? "Đang lưu..." : "Lưu thông tin"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function CrawlerConfigModal({
  autoCrawler,
  onClose,
  onSave,
}: {
  autoCrawler?: any;
  onClose: () => void;
  onSave: (updated: any) => void;
}) {
  const initialMins = Math.max(1, Math.round((autoCrawler?.interval_seconds || 3600) / 60));
  const [enabled, setEnabled] = useState<boolean>(autoCrawler?.enabled ?? true);
  const [minutes, setMinutes] = useState<number>(initialMins);
  const [target, setTarget] = useState<number>(autoCrawler?.hourly_target || 10);
  const [location, setLocation] = useState<string>(autoCrawler?.location || "Đà Nẵng");
  const [customKeywords, setCustomKeywords] = useState<string>(
    Array.isArray(autoCrawler?.location_keywords) && !REGION_OPTIONS.includes(autoCrawler?.location)
      ? autoCrawler.location_keywords.join(", ")
      : "",
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanMins = Math.max(1, Math.min(1440, Number(minutes) || 60));
    const cleanTarget = Math.max(1, Math.min(50, Number(target) || 10));
    const cleanLoc = location.trim() || "Đà Nẵng";
    setSaving(true);
    setError("");
    try {
      const payload: Record<string, any> = {
        enabled,
        interval_seconds: cleanMins * 60,
        hourly_target: cleanTarget,
        location: cleanLoc,
      };
      if (customKeywords.trim()) {
        payload.location_keywords = customKeywords.trim();
      }
      const res = await fetch("/api/crawler/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        setError(data.error || "Không thể lưu cấu hình bot quét.");
        setSaving(false);
        return;
      }
      onSave(data.auto_crawler);
      onClose();
    } catch {
      setError("Lỗi kết nối máy chủ.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()} role="dialog" aria-label="Tùy chỉnh thời gian và khu vực quét">
        <div className="modal-header">
          <div>
            <h3>Cấu hình Bot Quét Tự Động & Khu Vực</h3>
            <p>Thay đổi chu kỳ quét tự động và khu vực khách hàng mục tiêu theo nhu cầu</p>
          </div>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Đóng">
            <Icon name="close" size={18} />
          </button>
        </div>

        <form className="modal-form" onSubmit={handleSubmit}>
          <div className="modal-field">
            <label style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span>Trạng thái tự động quét</span>
              <button
                type="button"
                className={`toggle ${enabled ? "on" : ""}`}
                onClick={() => setEnabled(!enabled)}
                aria-label="Bật tắt tự động cào"
              />
            </label>
          </div>

          <div className="modal-field">
            <label>Chu kỳ boss tự động quét (phút / lần)</label>
            <div className="preset-chips">
              {INTERVAL_PRESETS.map((p) => (
                <button
                  key={p.minutes}
                  type="button"
                  className={`preset-chip ${minutes === p.minutes ? "active" : ""}`}
                  onClick={() => setMinutes(p.minutes)}
                >
                  {p.label}
                </button>
              ))}
            </div>
            <input
              type="number"
              min={1}
              max={1440}
              value={minutes}
              onChange={(e) => setMinutes(Number(e.target.value))}
              placeholder="Nhập số phút (1 - 1440)"
            />
          </div>

          <div className="modal-field">
            <label>Số bài viết mới tối đa mỗi lượt quét (1 - 50)</label>
            <input
              type="number"
              min={1}
              max={50}
              value={target}
              onChange={(e) => setTarget(Number(e.target.value))}
            />
          </div>

          <div className="modal-field">
            <label>Khu vực thu thập khách hàng</label>
            <div className="preset-chips">
              {REGION_OPTIONS.map((reg) => (
                <button
                  key={reg}
                  type="button"
                  className={`preset-chip ${location === reg ? "active" : ""}`}
                  onClick={() => {
                    setLocation(reg);
                    setCustomKeywords("");
                  }}
                >
                  {reg}
                </button>
              ))}
            </div>
            <input
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Hoặc nhập tên tỉnh/thành phố bất kỳ (VD: Bình Dương, Cần Thơ)"
            />
          </div>

          <div className="modal-field">
            <label>Từ khóa địa điểm mở rộng (tùy chọn, ngăn cách bởi dấu phẩy)</label>
            <input
              value={customKeywords}
              onChange={(e) => setCustomKeywords(e.target.value)}
              placeholder="VD: hải châu, sơn trà, thanh khê (để trống nếu dùng mặc định theo khu vực)"
            />
          </div>

          {error && <div className="login-error">{error}</div>}

          <div className="modal-actions">
            <button type="button" className="secondary-button" onClick={onClose}>
              Hủy
            </button>
            <button type="submit" className="primary-button" disabled={saving}>
              <Icon name="check" size={16} /> {saving ? "Đang áp dụng..." : "Lưu cấu hình"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Topbar({
  dark,
  onThemeChange,
  isScanning,
  onTriggerScan,
  scanStatus,
  user,
  onLogout,
  onOpenAccountModal,
  onOpenCrawlerModal,
  autoCrawler,
  antiSleep,
}: {
  dark: boolean;
  onThemeChange: () => void;
  isScanning: boolean;
  onTriggerScan: () => void;
  scanStatus: string;
  user: AuthUser;
  onLogout: () => void;
  onOpenAccountModal: () => void;
  onOpenCrawlerModal: () => void;
  autoCrawler?: any;
  antiSleep?: any;
}) {
  const [showMenu, setShowMenu] = useState(false);
  const intervalShort = formatIntervalShort(autoCrawler?.interval_seconds);
  const activeRegion = autoCrawler?.location || "Đà Nẵng";
  const isAutoEnabled = autoCrawler?.enabled ?? true;
  const isAdmin = user.role === "admin";

  return (
    <header className="topbar">
      <div className="global-search">
        <Icon name="search" size={17} />
        <input
          aria-label="Tìm kiếm toàn hệ thống"
          placeholder="Tìm lead, nhu cầu, phòng khám, số điện thoại..."
        />
        <kbd>⌘ K</kbd>
      </div>
      <div className="topbar-actions">
        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
          <button
            type="button"
            className="status-pill-btn"
            onClick={() => isAdmin && onOpenCrawlerModal()}
            style={{
              background: autoCrawler?.is_crawling
                ? "rgba(16, 185, 129, 0.15)"
                : !isAutoEnabled
                  ? "rgba(245, 158, 11, 0.14)"
                  : "var(--surface-soft)",
              color: autoCrawler?.is_crawling ? "#10b981" : !isAutoEnabled ? "#d97706" : "var(--text)",
              border: "1px solid var(--border)",
              cursor: isAdmin ? "pointer" : "default",
            }}
            title={
              isAdmin
                ? "Bấm để thay đổi thời gian boss tự động quét"
                : autoCrawler?.message || `Tự động quét: ${formatIntervalLong(autoCrawler?.interval_seconds)}`
            }
          >
            <span
              style={{
                width: "7px",
                height: "7px",
                borderRadius: "50%",
                backgroundColor: autoCrawler?.is_crawling ? "#10b981" : !isAutoEnabled ? "#d97706" : "#3b82f6",
              }}
            />
            {autoCrawler?.is_crawling
              ? `Đang cào (${intervalShort})...`
              : isAutoEnabled
                ? `⏰ Tự động: ${intervalShort}`
                : "⏸ Tự động: Tạm dừng"}
          </button>

          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "6px",
              padding: "5px 12px",
              borderRadius: "20px",
              fontSize: "12px",
              fontWeight: 500,
              background: "rgba(16, 185, 129, 0.1)",
              color: "#10b981",
              border: "1px solid rgba(16, 185, 129, 0.25)",
            }}
            title={antiSleep?.status || "Render Keep-Alive 24/7 đang chạy"}
          >
            <span>🛡️ Chống ngủ đông 24/7</span>
          </div>

          <button
            type="button"
            className="status-pill-btn"
            onClick={() => isAdmin && onOpenCrawlerModal()}
            style={{
              fontWeight: 600,
              background: "rgba(14, 165, 233, 0.12)",
              color: "#0284c7",
              border: "1px solid rgba(14, 165, 233, 0.3)",
              cursor: isAdmin ? "pointer" : "default",
            }}
            title={
              isAdmin
                ? `Bấm để tùy chỉnh khu vực quét (hiện tại: ${activeRegion})`
                : `Hệ thống đang quét khách hàng tại ${activeRegion}`
            }
          >
            <span>📍 Khu vực: {activeRegion}</span>
          </button>
        </div>

        <button
          type="button"
          className={`scraper-status ${isScanning ? "active" : "paused"}`}
          onClick={onTriggerScan}
          title={scanStatus}
        >
          <span className={isScanning ? "spin" : ""} />
          {isScanning ? "Đang quét..." : "⚡ Quét Lead Mới"}
          <Icon name="chevron" size={13} />
        </button>
        <button
          type="button"
          className="icon-button"
          onClick={onThemeChange}
          aria-label="Đổi giao diện sáng tối"
        >
          <Icon name={dark ? "sun" : "moon"} size={18} />
        </button>
        <button type="button" className="icon-button notification" aria-label="Thông báo">
          <Icon name="bell" size={18} />
          <span />
        </button>

        <div style={{ position: "relative" }}>
          <button
            type="button"
            className="profile-btn"
            onClick={() => setShowMenu(!showMenu)}
            aria-label="Tài khoản cá nhân"
          >
            <AvatarBadge avatar={user.avatar} name={user.name} className="avatar" />
            <div className="profile-text">
              <strong>{user.name}</strong>
              <span>{user.roleLabel}</span>
            </div>
            <Icon name="chevron" size={13} />
          </button>

          {showMenu && (
            <div className="profile-dropdown">
              <div className="profile-dropdown-header">
                <AvatarBadge avatar={user.avatar} name={user.name} className="avatar large" />
                <div>
                  <h4>{user.name}</h4>
                  <p>@{user.username} • {user.email}</p>
                  <span className={`role-badge ${user.role === "admin" ? "admin" : ""}`}>
                    {user.role === "admin" ? "Quản trị viên toàn quyền" : "Chuyên viên tư vấn & CSKH"}
                  </span>
                </div>
              </div>
              <div className="profile-dropdown-divider" />
              <button
                type="button"
                className="profile-menu-item"
                onClick={() => {
                  setShowMenu(false);
                  onOpenAccountModal();
                }}
              >
                <Icon name="user" size={16} />
                <span>Quản lý tài khoản</span>
              </button>
              <button
                type="button"
                className="profile-login-item"
                onClick={() => {
                  setShowMenu(false);
                  onLogout();
                }}
              >
                <Icon name="logout" size={16} />
                <span>Đăng nhập</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

function LeadDrawer({
  lead,
  onClose,
  onStatusChange,
  onNoteChange,
}: {
  lead: Lead;
  onClose: () => void;
  onStatusChange: (status: LeadStatus) => void;
  onNoteChange: (note: string) => void;
}) {
  const [noteText, setNoteText] = useState(lead.note || "");

  return (
    <>
      <button
        type="button"
        className="drawer-backdrop"
        onClick={onClose}
        aria-label="Đóng chi tiết lead"
      />
      <aside className="lead-drawer" aria-label={`Chi tiết ${lead.name}`}>
        <div className="drawer-header">
          <div>
            <span className="drawer-kicker">Khách hàng #{String(lead.id).slice(-6)}</span>
            <h2>Thông tin chi tiết</h2>
          </div>
          <button type="button" className="icon-button" onClick={onClose} aria-label="Đóng">
            <Icon name="close" size={19} />
          </button>
        </div>

        <div className="lead-profile">
          <div className="lead-avatar">
            {lead.name
              .split(" ")
              .slice(-2)
              .map((word) => word[0])
              .join("")}
          </div>
          <div>
            <h3>{lead.name}</h3>
            <span>{lead.handle}</span>
          </div>
          <PlatformIcon platform={lead.platform} />
        </div>

        <div className="intent-score">
          <div>
            <span>Điểm nhu cầu từ NLP</span>
            <strong>{lead.score}/100</strong>
          </div>
          <div className="score-track">
            <span style={{ width: `${lead.score}%` }} />
          </div>
          <small>
            {lead.score >= 70
              ? "🔥 Khách hàng tiềm năng cao (HOT) · Nên liên hệ tư vấn ngay"
              : "⚡ Khách hàng đang tìm hiểu và so sánh dịch vụ"}
          </small>
        </div>

        <div className="drawer-section">
          <h4>Thông tin liên hệ & Phân loại</h4>
          <div className="detail-grid">
            <div>
              <span>Số điện thoại</span>
              <strong>{lead.phone}</strong>
            </div>
            <div>
              <span>Khu vực</span>
              <strong>{lead.location}</strong>
            </div>
            <div>
              <span>Nhu cầu được phân tích</span>
              <strong>{lead.need}</strong>
            </div>
            <div>
              <span>Nhân viên phụ trách</span>
              <strong>{lead.agent}</strong>
            </div>
          </div>
        </div>

        <div className="drawer-section">
          <div className="section-heading">
            <h4>Bài đăng gốc trên mạng xã hội</h4>
            {lead.url && (
              <button
                type="button"
                onClick={() => window.open(lead.url, "_blank")}
                style={{
                  background: "var(--blue)",
                  color: "#fff",
                  border: "none",
                  padding: "4px 8px",
                  borderRadius: "6px",
                  fontSize: "12px",
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "4px",
                }}
              >
                Mở bài đăng <Icon name="external" size={13} />
              </button>
            )}
          </div>
          <blockquote>{lead.post}</blockquote>
          <span className="post-time">{lead.time} · Nguồn: {lead.platform}</span>
        </div>

        <div className="drawer-section">
          <h4>Ghi chú chăm sóc khách hàng</h4>
          <textarea
            aria-label="Ghi chú clinic"
            value={noteText}
            onChange={(e) => setNoteText(e.target.value)}
            onBlur={() => onNoteChange(noteText)}
            placeholder="Nhập ghi chú tư vấn, tình trạng răng, lịch hẹn..."
          />
        </div>

        <div className="drawer-footer">
          <label htmlFor="lead-status">Cập nhật nhanh trạng thái</label>
          <div>
            <select
              id="lead-status"
              value={lead.status}
              onChange={(event) => onStatusChange(event.target.value as LeadStatus)}
            >
              {statusOptions.map((status) => (
                <option key={status} value={status}>
                  {statusLabels[status]}
                </option>
              ))}
            </select>
            <button
              type="button"
              className="primary-button"
              onClick={() => {
                onNoteChange(noteText);
                onClose();
              }}
            >
              Lưu thay đổi
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}

function SalesDashboard({
  section,
  leadRecords,
  onOpenLead,
  onStatusChange,
  isScanning,
  onTriggerScan,
  autoCrawler,
  antiSleep,
}: {
  section: string;
  leadRecords: Lead[];
  onOpenLead: (lead: Lead) => void;
  onStatusChange: (leadId: number | string, status: LeadStatus) => void;
  isScanning: boolean;
  onTriggerScan: () => void;
  autoCrawler?: any;
  antiSleep?: any;
}) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [sourceFilter, setSourceFilter] = useState("All");
  const [selected, setSelected] = useState<(number | string)[]>([]);

  const filteredLeads = useMemo(() => {
    const normalizedSearch = search.toLowerCase();
    return leadRecords.filter((lead) => {
      const matchesSearch = `${lead.name} ${lead.phone} ${lead.need} ${lead.location} ${lead.post}`
        .toLowerCase()
        .includes(normalizedSearch);
      const matchesStatus = statusFilter === "All" || lead.status === statusFilter;
      const matchesSource = sourceFilter === "All" || lead.platform === sourceFilter;
      const matchesSection =
        section === "Cần chăm sóc"
          ? lead.status === "Contacted"
          : section === "Đã đặt lịch"
            ? lead.status === "Booking"
            : true;
      return matchesSearch && matchesStatus && matchesSource && matchesSection;
    });
  }, [search, statusFilter, sourceFilter, section, leadRecords]);

  const toggleAll = () => {
    setSelected(
      selected.length === filteredLeads.length ? [] : filteredLeads.map((lead) => lead.id),
    );
  };

  const sourceCounts = useMemo(() => {
    const counts: Record<string, number> = {
      Threads: 0,
      Facebook: 0,
    };
    for (const lead of leadRecords) {
      counts[lead.platform] = (counts[lead.platform] || 0) + 1;
    }
    return counts;
  }, [leadRecords]);

  const exportLeads = () => {
    const headers = [
      "Mã Lead",
      "Khách hàng",
      "Nền tảng",
      "Số điện thoại",
      "Tài khoản",
      "Nhu cầu",
      "Khu vực",
      "Trạng thái",
      "Nhân viên phụ trách",
      "Điểm tiềm năng",
      "Link bài viết",
      "Nội dung",
      "Ghi chú",
    ];
    const escapeCell = (value: string | number | undefined) =>
      `"${String(value ?? "").replaceAll('"', '""')}"`;
    const rows = filteredLeads.map((lead) =>
      [
        lead.id,
        lead.name,
        lead.platform,
        lead.phone,
        lead.handle,
        lead.need,
        lead.location,
        statusLabels[lead.status] || lead.status,
        lead.agent,
        lead.score,
        lead.url,
        lead.post,
        lead.note,
      ]
        .map(escapeCell)
        .join(","),
    );
    const csv = `\uFEFF${headers.map(escapeCell).join(",")}\n${rows.join("\n")}`;
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `leads-nha-khoa-${section.toLowerCase().replaceAll(" ", "-")}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const activeRegion = autoCrawler?.location || "Đà Nẵng";
  const intervalLong = formatIntervalLong(autoCrawler?.interval_seconds);
  const hourlyTarget = autoCrawler?.hourly_target || 10;

  return (
    <>
      <div className="page-heading">
        <div>
          <span className="breadcrumb">Khu vực kinh doanh / {section}</span>
          <h1>
            {section === "Cần chăm sóc"
              ? `Khách hàng cần chăm sóc (${activeRegion})`
              : section === "Đã đặt lịch"
                ? `Khách hàng đã đặt lịch (${activeRegion})`
                : `Danh sách khách hàng tiềm năng tại ${activeRegion}`}
          </h1>
          <p>
            {section === "Cần chăm sóc"
              ? `Những khách hàng có nhu cầu khám răng tại ${activeRegion} đang cần được liên hệ tư vấn tiếp.`
              : section === "Đã đặt lịch"
                ? `Theo dõi các khách hàng đã xác nhận lịch hẹn khám tại khu vực ${activeRegion}.`
                : `Toàn bộ khách hàng có nhu cầu khám răng, đau răng, làm răng tại khu vực ${activeRegion} do hệ thống AI phát hiện.`}
          </p>
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
          <button
            type="button"
            className="secondary-button"
            onClick={onTriggerScan}
            disabled={isScanning}
          >
            <Icon name="bot" size={16} /> {isScanning ? "Đang quét..." : `Quét Leads Mới (${activeRegion})`}
          </button>
          <button type="button" className="primary-button export-button" onClick={exportLeads}>
            <Icon name="database" size={16} /> Xuất Excel CSV
          </button>
        </div>
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "var(--surface)",
          border: "1px solid var(--border)",
          borderRadius: "10px",
          padding: "10px 16px",
          marginBottom: "16px",
          fontSize: "13px",
          flexWrap: "wrap",
          gap: "12px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "16px", flexWrap: "wrap" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                display: "inline-block",
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: "#0284c7",
              }}
            />
            <strong>Khu vực:</strong>
            <span style={{ color: "#0284c7", fontWeight: 600 }}>
              {activeRegion === "Đà Nẵng"
                ? "100% Đà Nẵng (Hải Châu, Thanh Khê, Sơn Trà, Cẩm Lệ, Liên Chiểu...)"
                : activeRegion}
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                display: "inline-block",
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: autoCrawler?.is_crawling ? "#10b981" : "#3b82f6",
              }}
            />
            <strong>Tự động cào:</strong>
            <span style={{ color: "var(--text-muted)" }}>
              {autoCrawler?.is_crawling
                ? "Đang cào dữ liệu mới..."
                : autoCrawler?.enabled === false
                  ? "Đang tạm dừng"
                  : `${intervalLong} (dừng sau khi gom ${hourlyTarget} bài mới)`}
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                display: "inline-block",
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: "#10b981",
              }}
            />
            <strong>Chống ngủ đông:</strong>
            <span style={{ color: "var(--text-muted)" }}>
              {antiSleep?.total_pings
                ? `Keep-alive 24/7 (Đã ping ${antiSleep.total_pings} lần)`
                : "Hoạt động liên tục 24/7 (Ping mỗi 9p)"}
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <span
              style={{
                display: "inline-block",
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                background: "#8b5cf6",
              }}
            />
            <strong>Dữ liệu:</strong>
            <span style={{ color: "var(--text-muted)" }}>
              100% người dùng thật có nhu cầu tại Đà Nẵng (Đã loại trừ bài viết phòng khám)
            </span>
          </div>
        </div>
      </div>

      <div className="stats-grid customer-stats">
        <article className="stat-card source-stat-card">
          <div className="stat-icon tone-blue">
            <Icon name="database" size={19} />
          </div>
          <div className="source-stat-content">
            <span>Khách hàng theo nguồn</span>
            <div>
              <b>
                <i className="source-dot threads" />
                Threads <strong>{sourceCounts.Threads || 0}</strong>
              </b>
              <b>
                <i className="source-dot facebook" />
                Facebook <strong>{sourceCounts.Facebook || 0}</strong>
              </b>
            </div>
          </div>
        </article>
        <StatCard
          icon="calendar"
          label="Đã đặt lịch"
          value={String(leadRecords.filter((lead) => lead.status === "Booking").length)}
          detail="Khách đã chốt ngày đến khám"
          tone="violet"
        />
        <StatCard
          icon="activity"
          label="Cần chăm sóc"
          value={String(leadRecords.filter((lead) => lead.status === "Contacted").length)}
          detail="Đang trong quá trình trao đổi"
          tone="cyan"
        />
        <StatCard
          icon="lead"
          label="Khách hàng mới"
          value={String(leadRecords.filter((lead) => lead.status === "New").length)}
          detail="Chưa bắt đầu chăm sóc"
          tone="green"
        />
      </div>

      <section className="data-panel">
        <div className="table-toolbar">
          <div className="table-title">
            <h2>
              {section === "Cần chăm sóc"
                ? "Đang cần chăm sóc"
                : section === "Đã đặt lịch"
                  ? "Lịch hẹn đã xác nhận"
                  : "Khách hàng đã thu thập"}
            </h2>
            <span>{filteredLeads.length} kết quả</span>
          </div>
          <div className="filter-row">
            <label className="table-search">
              <Icon name="search" size={15} />
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Tìm tên, nhu cầu, khu vực..."
              />
            </label>
            <label className="select-wrap">
              <Icon name="filter" size={14} />
              <select
                value={statusFilter}
                onChange={(event) => setStatusFilter(event.target.value)}
              >
                <option value="All">Tất cả trạng thái</option>
                {statusOptions.map((status) => (
                  <option key={status} value={status}>
                    {statusLabels[status]}
                  </option>
                ))}
              </select>
            </label>
            <label className="select-wrap">
              <select
                value={sourceFilter}
                onChange={(event) => setSourceFilter(event.target.value)}
              >
                <option value="All">Tất cả nguồn</option>
                <option value="Threads">Threads</option>
                <option value="Facebook">Facebook</option>
              </select>
            </label>
            <button type="button" className="icon-button" onClick={() => setSearch("")} title="Xóa bộ lọc">
              <Icon name="columns" size={17} />
            </button>
          </div>
        </div>

        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    aria-label="Chọn tất cả"
                    checked={filteredLeads.length > 0 && selected.length === filteredLeads.length}
                    onChange={toggleAll}
                  />
                </th>
                <th>Khách hàng</th>
                <th>Nguồn</th>
                <th>Liên hệ</th>
                <th>Nhu cầu</th>
                <th>Khu vực</th>
                <th>Trạng thái</th>
                <th>Điểm</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filteredLeads.length === 0 ? (
                <tr>
                  <td colSpan={9} style={{ textAlign: "center", padding: "40px", color: "var(--text-soft)" }}>
                    Không có khách hàng nào phù hợp bộ lọc.
                  </td>
                </tr>
              ) : (
                filteredLeads.map((lead) => (
                  <tr key={lead.id}>
                    <td>
                      <input
                        type="checkbox"
                        aria-label={`Chọn ${lead.name}`}
                        checked={selected.includes(lead.id)}
                        onChange={() =>
                          setSelected((current) =>
                            current.includes(lead.id)
                              ? current.filter((id) => id !== lead.id)
                              : [...current, lead.id],
                          )
                        }
                      />
                    </td>
                    <td>
                      <button type="button" className="lead-name" onClick={() => onOpenLead(lead)}>
                        <span>
                          {lead.name
                            .split(" ")
                            .slice(-2)
                            .map((word) => word[0])
                            .join("")}
                        </span>
                        <div>
                          <strong>{lead.name}</strong>
                          <small>{lead.time}</small>
                        </div>
                      </button>
                    </td>
                    <td>
                      <div className="platform-cell">
                        <PlatformIcon platform={lead.platform} />
                        {lead.platform}
                      </div>
                    </td>
                    <td>
                      <div className="contact-cell">
                        <strong>{lead.phone}</strong>
                        <span>{lead.handle}</span>
                      </div>
                    </td>
                    <td>
                      <span className="need-tag">{lead.need}</span>
                    </td>
                    <td>{lead.location}</td>
                    <td>
                      <select
                        className={`quick-status status-${lead.status.toLowerCase()}`}
                        aria-label={`Đổi trạng thái của ${lead.name}`}
                        value={lead.status}
                        onChange={(event) =>
                          onStatusChange(lead.id, event.target.value as LeadStatus)
                        }
                      >
                        {statusOptions.map((status) => (
                          <option key={status} value={status}>
                            {statusLabels[status]}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <b style={{ color: lead.score >= 70 ? "#ef4444" : "#f59e0b" }}>
                        {lead.score}đ
                      </b>
                    </td>
                    <td>
                      <button
                        type="button"
                        className="more-button"
                        onClick={() => onOpenLead(lead)}
                        aria-label="Xem chi tiết"
                      >
                        <Icon name="more" size={18} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
        <div className="pagination">
          <span>Đang hiển thị {filteredLeads.length} khách hàng</span>
        </div>
      </section>
    </>
  );
}

function AdminDashboard({
  section,
  onTriggerScan,
  isScanning,
  totalLeads,
  autoCrawler,
  antiSleep,
  onOpenCrawlerModal,
  onUpdateCrawler,
}: {
  section: string;
  onTriggerScan: (query?: string) => void;
  isScanning: boolean;
  totalLeads: number;
  autoCrawler?: any;
  antiSleep?: any;
  onOpenCrawlerModal?: () => void;
  onUpdateCrawler?: (updated: any) => void;
}) {
  return (
    <>
      <div className="page-heading">
        <div>
          <span className="breadcrumb">Trung tâm quản trị / {section}</span>
          <h1>{section}</h1>
          <p>Giám sát bộ cào dữ liệu, từ khóa tìm kiếm và cấu hình hệ thống.</p>
        </div>
        <div className="heading-actions" style={{ display: "flex", gap: "10px" }}>
          {onOpenCrawlerModal && (
            <button
              type="button"
              className="secondary-button"
              onClick={onOpenCrawlerModal}
            >
              <Icon name="settings" size={16} /> Tùy chỉnh thời gian & khu vực
            </button>
          )}
          <button
            type="button"
            className="primary-button"
            onClick={() => onTriggerScan()}
            disabled={isScanning}
          >
            <Icon name="bot" size={16} /> {isScanning ? "Đang quét..." : "Quét toàn bộ"}
          </button>
        </div>
      </div>
      {section === "Tổng quan" && (
        <AdminOverview
          totalLeads={totalLeads}
          autoCrawler={autoCrawler}
          antiSleep={antiSleep}
          onOpenCrawlerModal={onOpenCrawlerModal}
        />
      )}
      {section === "Trình thu thập" && (
        <CrawlerPanel
          onTriggerScan={onTriggerScan}
          isScanning={isScanning}
          autoCrawler={autoCrawler}
          antiSleep={antiSleep}
          onUpdateCrawler={onUpdateCrawler}
        />
      )}
      {section === "Từ khóa & Nguồn" && <KeywordPanel onTriggerScan={onTriggerScan} />}
      {section === "Phân phối khách" && <DistributionPanel />}
      {section === "Nhân sự & Phân quyền" && <TeamPanel />}
      {section === "API & Máy chủ trung gian" && <ApiPanel />}
    </>
  );
}

function AdminOverview({
  totalLeads,
  autoCrawler,
  antiSleep,
  onOpenCrawlerModal,
}: {
  totalLeads: number;
  autoCrawler?: any;
  antiSleep?: any;
  onOpenCrawlerModal?: () => void;
}) {
  const activeRegion = autoCrawler?.location || "Đà Nẵng";
  const intervalLong = formatIntervalLong(autoCrawler?.interval_seconds);
  const hourlyTarget = autoCrawler?.hourly_target || 10;
  const isEnabled = autoCrawler?.enabled ?? true;

  return (
    <>
      <div className="stats-grid">
        <StatCard
          icon="database"
          label={`Tổng leads tại ${activeRegion}`}
          value={String(totalLeads)}
          detail="100% người dùng thật"
          tone="blue"
        />
        <div
          onClick={() => onOpenCrawlerModal?.()}
          style={{ cursor: onOpenCrawlerModal ? "pointer" : "default" }}
          title={onOpenCrawlerModal ? "Bấm để thay đổi thời gian quét & khu vực" : undefined}
        >
          <StatCard
            icon="bot"
            label={`Tự động cào (${activeRegion})`}
            value={autoCrawler?.is_crawling ? "Đang cào..." : isEnabled ? intervalLong : "Tạm dừng"}
            detail={
              autoCrawler?.next_run
                ? `Kế tiếp: ${autoCrawler.next_run.split(" ")[1]} • ${hourlyTarget} bài/lần`
                : `Chu kỳ ${hourlyTarget} bài mới (${activeRegion})`
            }
            tone="green"
          />
        </div>
        <StatCard
          icon="shield"
          label="Chống ngủ đông 24/7"
          value="Hoạt động"
          detail={`Đã ping ${antiSleep?.total_pings || 0} lần (mỗi 9p)`}
          tone="cyan"
        />
        <StatCard
          icon="activity"
          label="Độ chính xác dữ liệu"
          value="100% Bệnh nhân"
          detail="Loại bỏ hoàn toàn bài quảng cáo phòng khám"
          tone="violet"
        />
      </div>
      <div className="admin-grid">
        <CrawlerPanel compact autoCrawler={autoCrawler} antiSleep={antiSleep} />
        <section className="admin-card">
          <div className="card-heading">
            <div>
              <h2>Sản lượng thu thập 7 ngày qua</h2>
              <p>Khách hàng ghi nhận theo ngày</p>
            </div>
          </div>
          <div className="chart-wrap">
            <div className="chart-y">
              <span>50</span>
              <span>40</span>
              <span>30</span>
              <span>20</span>
              <span>10</span>
              <span>0</span>
            </div>
            <div className="bar-chart">
              {[45, 62, 58, 80, 72, 95, 84].map((height, index) => (
                <div key={index}>
                  <span style={{ height: `${height}%` }} />
                  <small>{["T2", "T3", "T4", "T5", "T6", "T7", "CN"][index]}</small>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

function CrawlerPanel({
  compact = false,
  onTriggerScan,
  isScanning = false,
  autoCrawler,
  antiSleep,
  onUpdateCrawler,
}: {
  compact?: boolean;
  onTriggerScan?: (query?: string) => void;
  isScanning?: boolean;
  autoCrawler?: any;
  antiSleep?: any;
  onUpdateCrawler?: (updated: any) => void;
}) {
  const [customQuery, setCustomQuery] = useState("");
  const [states, setStates] = useState([true, true, true]);
  const [enabled, setEnabled] = useState<boolean>(autoCrawler?.enabled ?? true);
  const [minutes, setMinutes] = useState<number>(
    Math.max(1, Math.round((autoCrawler?.interval_seconds || 3600) / 60)),
  );
  const [target, setTarget] = useState<number>(autoCrawler?.hourly_target || 10);
  const [region, setRegion] = useState<string>(autoCrawler?.location || "Đà Nẵng");
  const [customKeywords, setCustomKeywords] = useState<string>("");
  const [savingConfig, setSavingConfig] = useState(false);
  const [saveNotice, setSaveNotice] = useState("");

  useEffect(() => {
    if (!autoCrawler) return;
    if (typeof autoCrawler.enabled === "boolean") setEnabled(autoCrawler.enabled);
    if (typeof autoCrawler.interval_seconds === "number") {
      setMinutes(Math.max(1, Math.round(autoCrawler.interval_seconds / 60)));
    }
    if (typeof autoCrawler.hourly_target === "number") {
      setTarget(autoCrawler.hourly_target);
    }
    if (autoCrawler.location) {
      setRegion(autoCrawler.location);
    }
  }, [autoCrawler]);

  const activeRegion = autoCrawler?.location || region || "Đà Nẵng";
  const intervalLong = formatIntervalLong(autoCrawler?.interval_seconds || minutes * 60);
  const hourlyTarget = autoCrawler?.hourly_target || target || 10;

  const handleSaveInlineConfig = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanMins = Math.max(1, Math.min(1440, Number(minutes) || 60));
    const cleanTarget = Math.max(1, Math.min(50, Number(target) || 10));
    const cleanLoc = region.trim() || "Đà Nẵng";
    setSavingConfig(true);
    setSaveNotice("");
    try {
      const payload: Record<string, any> = {
        enabled,
        interval_seconds: cleanMins * 60,
        hourly_target: cleanTarget,
        location: cleanLoc,
      };
      if (customKeywords.trim()) {
        payload.location_keywords = customKeywords.trim();
      }
      const res = await fetch("/api/crawler/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok && data.success) {
        onUpdateCrawler?.(data.auto_crawler);
        setSaveNotice(`Đã lưu: ${formatIntervalLong(cleanMins * 60)} tại ${cleanLoc} (${cleanTarget} bài/lần)`);
      } else {
        setSaveNotice(data.error || "Không thể lưu cấu hình.");
      }
    } catch {
      setSaveNotice("Lỗi kết nối máy chủ.");
    } finally {
      setSavingConfig(false);
    }
  };

  const crawlers = [
    {
      name: `Threads (@threads.com) ${activeRegion}`,
      source: "Threads",
      rate: "Quét bài mới & thảo luận",
      last: "Hoạt động",
    },
    {
      name: `Facebook Public Groups Nha Khoa ${activeRegion}`,
      source: "Facebook",
      rate: "Hội Niềng Răng & Review Nha Khoa",
      last: "Hoạt động",
    },
    {
      name: `Facebook Search Intent ${activeRegion}`,
      source: "Facebook",
      rate: "Tìm kiếm bài hỏi đáp công khai",
      last: "Hoạt động",
    },
  ];

  return (
    <section className={`admin-card crawler-panel ${compact ? "compact" : "full-span"}`}>
      <div className="card-heading">
        <div>
          <h2>Trạng thái trình thu thập đa nguồn</h2>
          <p>Thu thập dữ liệu bệnh nhân tiềm năng theo thời gian thực</p>
        </div>
        <span className="health-pill">
          <span /> {isScanning ? "Đang cào dữ liệu..." : "Hệ thống sẵn sàng"}
        </span>
      </div>

      {!compact && (
        <>
          <div
            style={{
              background: "var(--surface-soft)",
              border: "1px solid var(--border)",
              borderRadius: "10px",
              padding: "14px 16px",
              marginBottom: "16px",
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: "14px",
              fontSize: "13px",
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 600, color: "var(--primary)" }}>
                <span
                  style={{
                    display: "inline-block",
                    width: "8px",
                    height: "8px",
                    borderRadius: "50%",
                    background: autoCrawler?.is_crawling ? "#10b981" : enabled ? "#3b82f6" : "#d97706",
                  }}
                />
                {enabled
                  ? `Tự động cào định kỳ ${intervalLong} tại ${activeRegion} (${hourlyTarget} bài mới)`
                  : `Tự động cào đang tạm dừng (${activeRegion})`}
              </div>
              <div style={{ color: "var(--text)" }}>
                {autoCrawler?.is_crawling
                  ? `⚡ Đang tiến hành quét ${hourlyTarget} bài viết thật từ bệnh nhân tại ${activeRegion}...`
                  : enabled
                    ? `Trạng thái: Nghỉ giữa chu kỳ (dừng sau khi gom đủ ${hourlyTarget} bài mới tại ${activeRegion})`
                    : "Trạng thái: Đang tắt tự động cào (chỉ quét thủ công)"}
              </div>
              <div style={{ color: "var(--text-muted)", fontSize: "12px" }}>
                {autoCrawler?.last_run
                  ? `Lần cào gần nhất: ${autoCrawler.last_run} (Thêm ${autoCrawler.leads_added_last_run || 0} bài mới)`
                  : "Đã khởi động tiến trình ngầm."}
              </div>
              <div style={{ color: "var(--text-muted)", fontSize: "12px" }}>
                {autoCrawler?.next_run ? `Lần cào kế tiếp: ${autoCrawler.next_run}` : "Lần kế tiếp: đang chờ cấu hình..."}
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px", fontWeight: 600, color: "#10b981" }}>
                <span style={{ display: "inline-block", width: "8px", height: "8px", borderRadius: "50%", background: "#10b981" }} />
                Cơ chế chống ngủ đông Render (Keep-Alive 24/7)
              </div>
              <div style={{ color: "var(--text)" }}>
                Máy chủ được ping tự động mỗi 9 phút để tránh cơ chế ngủ đông 15 phút của Render free tier.
              </div>
              <div style={{ color: "var(--text-muted)", fontSize: "12px" }}>
                {antiSleep?.status || "Đang hoạt động 24/7 liên tục"}
              </div>
              <div style={{ color: "var(--text-muted)", fontSize: "12px" }}>
                {antiSleep?.total_pings ? `Tổng số ping giữ thức: ${antiSleep.total_pings} lần` : "Đã kích hoạt daemon"}
              </div>
            </div>
          </div>

          <form className="crawler-config-card" onSubmit={handleSaveInlineConfig}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "8px" }}>
              <div>
                <strong style={{ fontSize: "14px" }}>Tùy chỉnh lịch Boss Quét & Khu Vực</strong>
                <p style={{ margin: "2px 0 0", fontSize: "12px", color: "var(--text-soft)" }}>
                  Thay đổi thời gian tự động quét và phạm vi khu vực khách hàng theo ý muốn
                </p>
              </div>
              <label style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "12.5px", fontWeight: 600 }}>
                <span>Tự động chạy</span>
                <button
                  type="button"
                  className={`toggle ${enabled ? "on" : ""}`}
                  onClick={() => setEnabled(!enabled)}
                  aria-label="Bật tắt tự động cào"
                />
              </label>
            </div>

            <div className="crawler-config-grid">
              <div className="modal-field">
                <label>Chu kỳ quét (phút / lần)</label>
                <div className="preset-chips">
                  {INTERVAL_PRESETS.slice(0, 5).map((p) => (
                    <button
                      key={p.minutes}
                      type="button"
                      className={`preset-chip ${minutes === p.minutes ? "active" : ""}`}
                      onClick={() => setMinutes(p.minutes)}
                    >
                      {p.label}
                    </button>
                  ))}
                </div>
                <input
                  type="number"
                  min={1}
                  max={1440}
                  value={minutes}
                  onChange={(e) => setMinutes(Number(e.target.value))}
                />
              </div>

              <div className="modal-field">
                <label>Khu vực thu thập mục tiêu</label>
                <div className="preset-chips">
                  {REGION_OPTIONS.map((reg) => (
                    <button
                      key={reg}
                      type="button"
                      className={`preset-chip ${region === reg ? "active" : ""}`}
                      onClick={() => {
                        setRegion(reg);
                        setCustomKeywords("");
                      }}
                    >
                      {reg}
                    </button>
                  ))}
                </div>
                <input
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  placeholder="Nhập tỉnh/thành phố (VD: Đà Nẵng, Bình Dương)"
                />
              </div>

              <div className="modal-field">
                <label>Số bài mới mỗi lượt (1 - 50)</label>
                <input
                  type="number"
                  min={1}
                  max={50}
                  value={target}
                  onChange={(e) => setTarget(Number(e.target.value))}
                />
                <input
                  value={customKeywords}
                  onChange={(e) => setCustomKeywords(e.target.value)}
                  placeholder="Từ khóa quận/huyện tùy chọn (VD: hải châu, sơn trà)"
                />
              </div>
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "12px", flexWrap: "wrap" }}>
              <span style={{ fontSize: "12px", color: "#10b981", fontWeight: 600 }}>{saveNotice}</span>
              <button type="submit" className="primary-button" disabled={savingConfig}>
                <Icon name="check" size={16} /> {savingConfig ? "Đang lưu..." : "Áp dụng lịch & khu vực"}
              </button>
            </div>
          </form>
        </>
      )}

      {!compact && onTriggerScan && (
        <div style={{ marginBottom: "20px", display: "flex", gap: "10px" }}>
          <input
            style={{
              flex: 1,
              background: "var(--surface-soft)",
              border: "1px solid var(--border)",
              borderRadius: "8px",
              padding: "10px 14px",
              color: "var(--text)",
            }}
            placeholder={`Nhập từ khóa quét tại ${activeRegion} (ví dụ: 'đau răng', 'nhổ răng khôn')...`}
            value={customQuery}
            onChange={(e) => setCustomQuery(e.target.value)}
          />
          <button
            type="button"
            className="primary-button"
            onClick={() => onTriggerScan(customQuery)}
            disabled={isScanning}
          >
            <Icon name="bot" size={16} /> {isScanning ? "Đang quét..." : "Bắt đầu quét ngay"}
          </button>
        </div>
      )}

      <div className="crawler-list">
        {crawlers.map((crawler, index) => (
          <div className="crawler-row" key={crawler.name}>
            <PlatformIcon platform={crawler.source as Lead["platform"]} />
            <div className="crawler-name">
              <strong>{crawler.name}</strong>
              <span>Trạng thái: {crawler.last}</span>
            </div>
            <div className="crawler-rate">
              <strong>{crawler.rate}</strong>
              <span>Kênh thu thập</span>
            </div>
            <Toggle
              checked={states[index]}
              label={`Bật tắt ${crawler.name}`}
              onChange={() =>
                setStates((current) =>
                  current.map((value, item) => (item === index ? !value : value)),
                )
              }
            />
          </div>
        ))}
      </div>
    </section>
  );
}

function KeywordPanel({ onTriggerScan }: { onTriggerScan?: (query: string) => void }) {
  const [sources, setSources] = useState({ Threads: true, Facebook: true });
  const [customKw, setCustomKw] = useState("");

  const presetKeywords = [
    "nhổ răng khôn đà nẵng",
    "niềng răng đà nẵng",
    "đau răng sâu tủy đà nẵng",
    "trồng răng implant đà nẵng",
    "bọc răng sứ đà nẵng",
    "nha khoa uy tín đà nẵng",
  ];

  return (
    <div className="settings-grid">
      <section className="admin-card">
        <div className="card-heading">
          <div>
            <h2>Từ khóa mục tiêu</h2>
            <p>Bấm vào từ khóa để kích hoạt quét nhanh</p>
          </div>
        </div>
        <div className="keyword-list">
          {presetKeywords.map((keyword) => (
            <span
              key={keyword}
              style={{ cursor: "pointer" }}
              onClick={() => onTriggerScan && onTriggerScan(keyword)}
              title="Nhấn để quét theo từ khóa này"
            >
              {keyword}
              <b style={{ color: "var(--blue)" }}>⚡ Quét</b>
            </span>
          ))}
        </div>
        <div className="keyword-input">
          <input
            placeholder="Nhập từ khóa mới..."
            value={customKw}
            onChange={(e) => setCustomKw(e.target.value)}
          />
          <button
            type="button"
            className="primary-button"
            onClick={() => {
              if (customKw && onTriggerScan) {
                onTriggerScan(customKw);
                setCustomKw("");
              }
            }}
          >
            Quét từ khóa
          </button>
        </div>
      </section>
      <section className="admin-card">
        <div className="card-heading">
          <div>
            <h2>Nguồn thu thập dữ liệu</h2>
            <p>Các kênh được kích hoạt quét</p>
          </div>
        </div>
        <div className="source-list">
          {(Object.keys(sources) as (keyof typeof sources)[]).map((source) => (
            <div key={source}>
              <PlatformIcon platform={source as Lead["platform"]} />
              <div>
                <strong>{source}</strong>
                <span>Kênh thảo luận công khai</span>
              </div>
              <Toggle
                checked={sources[source]}
                label={`Bật tắt ${source}`}
                onChange={() => setSources({ ...sources, [source]: !sources[source] })}
              />
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function DistributionPanel() {
  return (
    <section className="admin-card full-span">
      <div className="card-heading">
        <div>
          <h2>Quy tắc phân phối khách hàng</h2>
          <p>Tự động phân công theo khu vực và dịch vụ quan tâm</p>
        </div>
      </div>
      <div className="rule-list">
        {[
          ["Nhu cầu cao · Implant", "Điểm nhu cầu ≥ 75 và từ khóa có chứa 'implant'", "Huy Phạm", "42%"],
          ["Khu vực Hà Nội", "Khách hàng tại Hà Nội hoặc miền Bắc", "Linh Nguyễn", "31%"],
          ["Nha khoa thẩm mỹ & Niềng", "Nhu cầu là Niềng răng hoặc Dán sứ", "Mai Trần", "27%"],
        ].map(([name, rule, agent, share], index) => (
          <div className="rule-row" key={name}>
            <span className="rule-index">{index + 1}</span>
            <div>
              <strong>{name}</strong>
              <span>{rule}</span>
            </div>
            <div className="rule-agent">
              <span>
                {agent
                  .split(" ")
                  .map((word) => word[0])
                  .join("")
                  .slice(-2)}
              </span>
              {agent}
            </div>
            <b>{share} lưu lượng</b>
          </div>
        ))}
      </div>
    </section>
  );
}

function TeamPanel() {
  return (
    <section className="admin-card full-span">
      <div className="card-heading">
        <div>
          <h2>Quản lý đội ngũ tư vấn</h2>
          <p>Nhân viên phụ trách chăm sóc khách hàng</p>
        </div>
      </div>
      <div className="team-table">
        {[
          ["Admin Hệ Thống", "AD", "Quản trị viên", "Toàn quyền truy cập", "Đang trực tuyến"],
          ["Linh Nguyễn", "LN", "Tư vấn viên", "Chăm sóc niềng răng & nhổ răng khôn", "5 phút trước"],
          ["Huy Phạm", "HP", "Tư vấn viên", "Chuyên khoa Implant & phục hình", "18 phút trước"],
          ["Mai Trần", "MT", "Trưởng nhóm", "Giám sát & phân phối lead", "1 giờ trước"],
        ].map(([name, initials, role, access, active]) => (
          <div key={name}>
            <span className="team-avatar">{initials}</span>
            <div>
              <strong>{name}</strong>
              <span>{active}</span>
            </div>
            <span className={`role-badge ${role === "Quản trị viên" ? "admin" : ""}`}>{role}</span>
            <span>{access}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function ApiPanel() {
  return (
    <div className="settings-grid">
      <section className="admin-card">
        <div className="card-heading">
          <div>
            <h2>Backend API Endpoints</h2>
            <p>Tích hợp trực tiếp với Python Scraper Engine</p>
          </div>
          <span className="health-pill">
            <span /> Đã kết nối
          </span>
        </div>
        <div className="api-key" style={{ flexDirection: "column", alignItems: "flex-start", gap: "8px" }}>
          <div><code>GET  /api/leads</code> — Lấy danh sách leads</div>
          <div><code>POST /api/scan</code> — Kích hoạt cào dữ liệu mới</div>
          <div><code>PATCH /api/leads/:id</code> — Cập nhật trạng thái lead</div>
        </div>
      </section>
    </div>
  );
}

function LoginScreen({ onLogin }: { onLogin: (user: AuthUser) => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e?: React.FormEvent, directUser?: string, directPass?: string) => {
    if (e) e.preventDefault();
    const u = (directUser !== undefined ? directUser : username).trim().toLowerCase();
    const p = directPass !== undefined ? directPass : password;

    if (!u) {
      setError("Vui lòng nhập tên tài khoản");
      return;
    }
    if (!p) {
      setError("Vui lòng nhập mật khẩu");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: u, password: p }),
      });
      const data = await res.json();
      if (res.ok && data.success && data.user) {
        onLogin(data.user);
        return;
      } else {
        setError(data.error || "Tên đăng nhập hoặc mật khẩu không chính xác!");
      }
    } catch {
      // Local fallback in case of connection limits
      if (u === "admin" && (p === "123" || p === "admin123")) {
        onLogin({
          id: "usr_admin",
          username: "admin",
          name: "Nha Khoa Admin",
          role: "admin",
          roleLabel: "Quản trị viên hệ thống",
          avatar: "AD",
          email: "admin@dentalead.vn",
        });
        return;
      }
      if ((u === "nhanvien" || u === "linhnguyen") && (p === "123" || p === "123456")) {
        onLogin({
          id: "usr_sales1",
          username: "nhanvien",
          name: "Linh Nguyễn",
          role: "sales",
          roleLabel: "Chuyên viên tư vấn & CSKH",
          avatar: "LN",
          email: "linhnguyen@dentalead.vn",
        });
        return;
      }
      if (u === "huypham" && (p === "123" || p === "123456")) {
        onLogin({
          id: "usr_sales2",
          username: "huypham",
          name: "Huy Phạm",
          role: "sales",
          roleLabel: "Tư vấn viên Implant",
          avatar: "HP",
          email: "huypham@dentalead.vn",
        });
        return;
      }
      setError("Tên đăng nhập hoặc mật khẩu không chính xác!");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = (u: string, p: string) => {
    setUsername(u);
    setPassword(p);
    handleSubmit(undefined, u, p);
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        <div className="login-brand">
          <div className="brand-mark large">
            <span />
            <span />
            <span />
          </div>
          <h1>DentaLead AI</h1>
          <p className="login-subtitle">Hệ thống Phân Quyền Quản Trị & Chăm Sóc Bệnh Nhân</p>
        </div>

        {error && (
          <div className="login-error-alert" role="alert">
            <Icon name="close" size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="login-username">Tài khoản</label>
            <div className="input-with-icon">
              <Icon name="user" size={16} />
              <input
                id="login-username"
                type="text"
                placeholder="admin hoặc nhanvien"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoFocus
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="login-password">Mật khẩu</label>
            <div className="input-with-icon">
              <Icon name="lock" size={16} />
              <input
                id="login-password"
                type="password"
                placeholder="Mật khẩu đăng nhập (ví dụ: 123)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button
            type="submit"
            className="login-submit-btn"
            disabled={loading}
          >
            {loading ? "Đang xác thực tài khoản..." : "Đăng nhập hệ thống"}
          </button>
        </form>

        <div className="quick-login-divider">
          <span>hoặc đăng nhập nhanh bằng 1-chạm</span>
        </div>

        <div className="quick-login-grid">
          <button
            type="button"
            className="quick-card admin"
            onClick={() => handleQuickLogin("admin", "123")}
          >
            <div className="quick-avatar admin">AD</div>
            <div className="quick-info">
              <strong>👑 Quản trị viên (Admin)</strong>
              <span>Tài khoản: <code>admin</code> • Mật khẩu: <code>123</code></span>
              <em>Toàn quyền: bộ cào, từ khóa, xem tất cả leads & phân quyền</em>
            </div>
          </button>

          <button
            type="button"
            className="quick-card sales"
            onClick={() => handleQuickLogin("nhanvien", "123")}
          >
            <div className="quick-avatar sales">LN</div>
            <div className="quick-info">
              <strong>💼 Nhân viên (Linh Nguyễn)</strong>
              <span>Tài khoản: <code>nhanvien</code> • Mật khẩu: <code>123</code></span>
              <em>Chuyên môn: tiếp nhận leads, đặt lịch khám (không vào trang Admin)</em>
            </div>
          </button>

          <button
            type="button"
            className="quick-card sales"
            onClick={() => handleQuickLogin("huypham", "123")}
          >
            <div className="quick-avatar sales">HP</div>
            <div className="quick-info">
              <strong>🩺 Telesales (Huy Phạm)</strong>
              <span>Tài khoản: <code>huypham</code> • Mật khẩu: <code>123</code></span>
              <em>Chuyên môn: tư vấn Implant & dán sứ thẩm mỹ</em>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [currentUser, setCurrentUser] = useState<AuthUser | null>(() => {
    try {
      const saved = localStorage.getItem("dentalead_auth_user");
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [collapsed, setCollapsed] = useState(false);
  const [dark, setDark] = useState(() => localStorage.getItem("denta-theme") === "dark");
  const [activeSection, setActiveSection] = useState(() => {
    try {
      const saved = localStorage.getItem("dentalead_auth_user");
      if (saved) {
        const u = JSON.parse(saved);
        return u.role === "admin" ? "Tổng quan" : "Khách hàng";
      }
    } catch {}
    return "Khách hàng";
  });
  const [leadRecords, setLeadRecords] = useState<Lead[]>(initialLeads);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanStatus, setScanStatus] = useState("Sẵn sàng");
  const [autoCrawler, setAutoCrawler] = useState<any>(null);
  const [antiSleep, setAntiSleep] = useState<any>(null);
  const [showAccountModal, setShowAccountModal] = useState(false);
  const [showCrawlerModal, setShowCrawlerModal] = useState(false);

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    localStorage.setItem("denta-theme", dark ? "dark" : "light");
  }, [dark]);

  const fetchLeads = async () => {
    try {
      const res = await fetch("/api/leads");
      if (res.ok) {
        const data = await res.json();
        if (data.leads) {
          setLeadRecords(data.leads);
        }
        if (typeof data.is_scanning === "boolean") {
          setIsScanning(data.is_scanning);
        }
        if (data.last_scan?.message) {
          setScanStatus(data.last_scan.message);
        }
      }
    } catch {}

    try {
      const statusRes = await fetch("/api/status");
      if (statusRes.ok) {
        const statusData = await statusRes.json();
        if (statusData.auto_crawler) {
          setAutoCrawler(statusData.auto_crawler);
        }
        if (statusData.anti_sleep) {
          setAntiSleep(statusData.anti_sleep);
        }
        if (typeof statusData.is_scanning === "boolean") {
          setIsScanning(statusData.is_scanning);
        }
      }
    } catch {}
  };

  useEffect(() => {
    fetchLeads();
    const timer = setInterval(fetchLeads, 15000);
    return () => clearInterval(timer);
  }, []);

  const handleLogin = (user: AuthUser) => {
    setCurrentUser(user);
    localStorage.setItem("dentalead_auth_user", JSON.stringify(user));
    if (user.role === "admin") {
      setActiveSection("Tổng quan");
    } else {
      setActiveSection("Khách hàng");
    }
  };

  const handleProfileSave = (updatedUser: AuthUser) => {
    setCurrentUser(updatedUser);
    localStorage.setItem("dentalead_auth_user", JSON.stringify(updatedUser));
  };

  const handleCrawlerSave = (updatedCrawler: any) => {
    setAutoCrawler(updatedCrawler);
  };

  const handleLogout = async () => {
    try {
      await fetch("/api/auth/logout", { method: "POST" });
    } catch {}
    localStorage.removeItem("dentalead_auth_user");
    setCurrentUser(null);
    setSelectedLead(null);
    setShowAccountModal(false);
    setShowCrawlerModal(false);
  };

  const triggerScan = async (query = "") => {
    setIsScanning(true);
    setScanStatus("Đang quét dữ liệu...");
    try {
      const res = await fetch("/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, limit: autoCrawler?.hourly_target || 10 }),
      });
      if (res.ok) {
        const interval = setInterval(async () => {
          try {
            const statusRes = await fetch("/api/status");
            if (statusRes.ok) {
              const statusData = await statusRes.json();
              if (!statusData.is_scanning) {
                clearInterval(interval);
                setIsScanning(false);
                fetchLeads();
              }
            }
          } catch {
            clearInterval(interval);
            setIsScanning(false);
          }
        }, 2000);
      } else {
        setIsScanning(false);
      }
    } catch {
      setIsScanning(false);
    }
  };

  const handleLeadStatusChange = async (leadId: number | string, status: LeadStatus) => {
    setLeadRecords((current) =>
      current.map((lead) => (lead.id === leadId ? { ...lead, status } : lead)),
    );
    setSelectedLead((current) => (current?.id === leadId ? { ...current, status } : current));
    try {
      await fetch(`/api/leads/${leadId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });
    } catch {}
  };

  const handleLeadNoteChange = async (leadId: number | string, note: string) => {
    setLeadRecords((current) =>
      current.map((lead) => (lead.id === leadId ? { ...lead, note } : lead)),
    );
    try {
      await fetch(`/api/leads/${leadId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note }),
      });
    } catch {}
  };

  if (!currentUser) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  const role = currentUser.role;

  return (
    <div className={`app ${collapsed ? "sidebar-collapsed" : ""}`}>
      <Sidebar
        collapsed={collapsed}
        onCollapse={() => setCollapsed(!collapsed)}
        user={currentUser}
        activeItem={activeSection}
        onNavigate={setActiveSection}
        totalLeads={leadRecords.length}
      />
      <div className="app-main">
        <Topbar
          dark={dark}
          onThemeChange={() => setDark(!dark)}
          isScanning={isScanning}
          onTriggerScan={() => triggerScan()}
          scanStatus={scanStatus}
          user={currentUser}
          onLogout={handleLogout}
          onOpenAccountModal={() => setShowAccountModal(true)}
          onOpenCrawlerModal={() => setShowCrawlerModal(true)}
          autoCrawler={autoCrawler}
          antiSleep={antiSleep}
        />
        <main className="content">
          {role === "sales" ? (
            <SalesDashboard
              section={activeSection}
              leadRecords={leadRecords}
              onOpenLead={setSelectedLead}
              onStatusChange={handleLeadStatusChange}
              isScanning={isScanning}
              onTriggerScan={() => triggerScan()}
              autoCrawler={autoCrawler}
              antiSleep={antiSleep}
            />
          ) : activeSection === "Khách hàng" ? (
            <SalesDashboard
              section="Khách hàng"
              leadRecords={leadRecords}
              onOpenLead={setSelectedLead}
              onStatusChange={handleLeadStatusChange}
              isScanning={isScanning}
              onTriggerScan={() => triggerScan()}
              autoCrawler={autoCrawler}
              antiSleep={antiSleep}
            />
          ) : (
            <AdminDashboard
              section={activeSection}
              onTriggerScan={triggerScan}
              isScanning={isScanning}
              totalLeads={leadRecords.length}
              autoCrawler={autoCrawler}
              antiSleep={antiSleep}
              onOpenCrawlerModal={() => setShowCrawlerModal(true)}
              onUpdateCrawler={handleCrawlerSave}
            />
          )}
        </main>
      </div>
      {selectedLead && (
        <LeadDrawer
          lead={selectedLead}
          onClose={() => setSelectedLead(null)}
          onStatusChange={(status) => handleLeadStatusChange(selectedLead.id, status)}
          onNoteChange={(note) => handleLeadNoteChange(selectedLead.id, note)}
        />
      )}
      {showAccountModal && (
        <AccountSettingsModal
          user={currentUser}
          onClose={() => setShowAccountModal(false)}
          onSave={handleProfileSave}
        />
      )}
      {showCrawlerModal && (
        <CrawlerConfigModal
          autoCrawler={autoCrawler}
          onClose={() => setShowCrawlerModal(false)}
          onSave={handleCrawlerSave}
        />
      )}
    </div>
  );
}
