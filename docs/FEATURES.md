# Документация по реализации функций BridgeGram (Мод Telegram)

## 1. Tor-сеть и мосты (Failover & Auto-Update)

В исходном коде Telegram (например, в `ConnectionsManager` или в сетевом слое `tgnet`) нужно добавить логику проверки файла `bridges.json` с репозитория.

### Авто-обновление
Реализовать задачу `AlarmManager` или `WorkManager`, которая каждые 10 минут обращается к:
`https://raw.githubusercontent.com/ktoto1300/tg-bridges/main/bridges.json`

### Failover
В методе, отвечающем за разрыв соединения (например, когда сокет кидает Timeout/Exception), добавить перехватчик:
```java
if (currentProxyType == PROXY_TYPE_AUTO_TOR) {
    String newBridge = BridgeManager.getNextBridge();
    applyProxyConfiguration(newBridge);
    reconnect();
}
```

## 2. Premium система и проверки

Для проверки ID пользователя:
```java
long currentUserId = UserConfig.getInstance(currentAccount).getClientUserId();
boolean isPremium = Arrays.asList(PREMIUM_IDS).contains(currentUserId);

if (!isPremium) {
    // Скрыть функции мода
}
```

На кнопке "Купить Premium" (в интерфейсе настроек):
```java
buyPremiumCell.setText("Скоро будет");
buyPremiumCell.setOnClickListener(v -> Toast.makeText(context, "Premium функционал в разработке.", Toast.LENGTH_SHORT).show());
```

Вывод User ID в настройках:
```java
// Добавить новую ячейку в SettingsActivity
TextDetailSettingsCell idCell = new TextDetailSettingsCell(context);
idCell.setTextAndValue("Ваш User ID", String.valueOf(currentUserId), true);
idCell.setOnClickListener(v -> {
    ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
    ClipData clip = ClipData.newPlainText("User ID", String.valueOf(currentUserId));
    clipboard.setPrimaryClip(clip);
    Toast.makeText(context, "ID скопирован", Toast.LENGTH_SHORT).show();
});
```

## 3. Настройки мода (Native Theme)

Все интерфейсы мода должны наследоваться от стандартных компонентов Telegram (например, `BaseFragment`). Цвета использовать из `Theme.getColor()`:
```java
cell.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundWhite));
cell.getTextView().setTextColor(Theme.getColor(Theme.key_windowBackgroundWhiteBlackText));
```

## 4. Основной функционал мода

### Anti-Delete
При получении `TLRPC.TL_updateDeleteMessages`:
Вместо удаления из локальной БД, помечать сообщение флагом `is_deleted = 1` и отображать в UI со специальной иконкой (например, красной корзиной).

### Ghost Mode
Блокировать отправку `TLRPC.TL_messages_readHistory` и `TLRPC.TL_messages_readMessageContents`.
```java
if (GhostModeConfig.isEnabled()) {
    // Не отправлять запрос на сервер
    return;
}
```

### No-Typing
В методе `MessagesController.getInstance(currentAccount).sendTyping(...)`:
```java
if (NoTypingConfig.isEnabled()) {
    return; // Отмена отправки статуса
}
```

### Anti-Restrict
В UI (фото/видео вьюверы) снять ограничения:
```java
// Найти проверки вроде messageObject.isRestricted() или hasNoforwards
// Заменить логику на:
boolean canCopy = true; // Вместо оригинальной проверки
```

## 5. Проверка обновлений APK

При старте приложения проверять:
`https://raw.githubusercontent.com/ktoto1300/tg-bridges/main/version.json`
Сравнивать `latest_version` с текущей версией. Если больше - показывать диалог с кнопкой обновления (скачивание из `update_url`).
