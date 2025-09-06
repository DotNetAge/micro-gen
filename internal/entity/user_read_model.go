package projection

import (
	"time"
	"test-local/internal/entity"
	"test-local/internal/entity/projection"
)

// UserReadModel User聚合的读模型实体
type UserReadModel struct {
	*projection.ReadModel
	
	// 业务字段
	Userid string `json:"user_id"`
	Username string `json:"username"`
	Email entity.Email `json:"email"`
	Address entity.Address `json:"address"`
	Phone entity.Phone `json:"phone"`
	Createdat time.Time `json:"created_at"`
	Updatedat time.Time `json:"updated_at"`
}

// NewUserReadModel 创建User读模型
func NewUserReadModel(id string) *UserReadModel {
	return &UserReadModel{
		ReadModel: projection.NewReadModel(id, "user"),
	}
}

// ApplyEvent 应用领域事件到读模型
func (m *UserReadModel) ApplyEvent(event entity.DomainEvent) error {
	switch event.GetEventType() {
	case "UserCreated":
		return m.applyCreated(event)
	case "UserUpdated":
		return m.applyUpdated(event)
	case "UserDeleted":
		return m.applyDeleted(event)
	default:
		return nil // 忽略不相关事件
	}
}

func (m *UserReadModel) applyCreated(event entity.DomainEvent) error {
	// 从事件数据填充业务字段
	data := event.GetData()
	
	// TODO: 根据实际事件结构填充字段
	// 示例：
	// if name, ok := data["name"]; ok {
	// 	m.Name = name.(string)
	// }
	
	return nil
}

func (m *UserReadModel) applyUpdated(event entity.DomainEvent) error {
	// 从事件数据更新业务字段
	data := event.GetData()
	
	// TODO: 根据实际事件结构更新字段
	_ = data
	
	return nil
}

func (m *UserReadModel) applyDeleted(event entity.DomainEvent) error {
	// 标记为已删除或清理数据
	// 可以设置删除标记或清空字段
	return nil
}