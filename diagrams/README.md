# diagrams/
图表源文件 + 渲染输出

- `plantuml/` `.puml` 源文件 (本地版本控制, 方便协作修改)
- `exported/` 渲染后的 `.png` / `.svg` (备份, 万一 plantuml 公网服务挂了可以用)

PlantUML 渲染优先用运行时 CDN, 这里的 exported 仅作离线备份。
