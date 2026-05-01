# 🛠️ 工具箱：Skill 进化工具

本目录用于管理 mao-skill 的进化工具。

---

## nuwa-skill (女娲造人)

**仓库**: https://github.com/alchaincyf/nuwa-skill

**用途**: 蒸馏人物的思维框架，生成新的 Skill

**加载方式**:
```
/skill https://github.com/alchaincyf/nuwa-skill
```

**场景**:
- 想扩展 mao-skill 的某个方面 → 用 nuwa 重新蒸馏
- 想添加新人物视角 → 用 nuwa 造新 Skill

---

## darwin-skill (达尔文)

**仓库**: https://github.com/alchaincyf/darwin-skill

**用途**: 评估和自动优化 Skill 质量（8维度评分）

**加载方式**:
```
/skill https://github.com/alchaincyf/darwin-skill
```

**场景**:
- 想评估 mao-skill 当前的评分 → 用 darwin 跑 8 维度评估
- 想自动优化 mao-skill → 让 darwin 执行优化循环

---

## 🔄 进化工作流

```
1. 手动修改 or 扩展 mao-skill 内容
         ↓
2. 用 darwin-skill 评估质量 (8维度评分)
         ↓
3. 根据评分优化 (结构/实测表现)
         ↓
4. 满意后 → 提交发布
         ↓
5. 如需扩展新内容 → 用 nuwa-skill 蒸馏
         ↓
6. 合并回 mao-skill
         ↓
7. 循环往复，持续进化
```

### darwin 评估维度

| 维度 | 分数 | 说明 |
|------|------|------|
| 1. Frontmatter质量 | /10 | name规范、description完整 |
| 2. 工作流清晰度 | /15 | 步骤明确可执行 |
| 3. 边界条件覆盖 | /10 | 异常处理、fallback |
| 4. 检查点设计 | /7 | 关键决策确认 |
| 5. 指令具体性 | /15 | 不模糊、有示例 |
| 6. 资源整合度 | /5 | 引用路径正确 |
| 7. 整体架构 | /15 | 结构清晰不冗余 |
| 8. 实测表现 | /25 | 跑测试看实际效果 |

---

## 📌 快速使用

```bash
# 1. 评估当前 mao-skill 质量
# 加载 darwin-skill，然后让它评估 ../mao-skill/SKILL.md

# 2. 根据评分优化
# 修改 SKILL.md 后重复评估

# 3. 如需扩展新内容
# 加载 nuwa-skill，让它蒸馏新主题
# 然后把结果合并回 mao-skill
```