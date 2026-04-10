# 获取设备序列号

## 前提条件

- 已安装 Dot. App
- 已登录 Dot. 账号
- 账号下至少有一台设备

## 步骤

### 1. 前往「更多」标签页

打开 Dot. App，点击底部导航栏的「更多」标签页。

### 2. 进入设备列表

点击头像下方的设备列表，查看您的所有设备。

### 3. 选择设备

点击您想要控制的设备，进入设备详情页面。

### 4. 复制设备序列号

在设备详情页面，向下滚动找到「设备序列号」部分：

- 点击「设备序列号」
- 序列号将自动复制到剪贴板

设备序列号格式类似：`ABCD1234ABCD`

## 使用设备序列号

获取设备序列号后，您可以在 API 请求中使用它：

```bash
curl -X GET \
  https://dot.mindreset.tech/api/authV2/open/device/ABCD1234ABCD/status \
  -H 'Authorization: Bearer dot_app_<您的密钥>'
```

## 下一步

现在您已经拥有：

- ✅ API 密钥
- ✅ 设备序列号

可以开始使用 Dot. OpenAPI 了！查看 [API 参考文档](../skills/dot-openapi/references/api_reference.md) 了解所有可用的接口。
