package projection

import (
	"time"
	"test-local/internal/entity"
	"test-local/internal/entity/projection"
)

// OrderReadModel Order聚合的读模型实体
type OrderReadModel struct {
	*projection.ReadModel
	
	// 业务字段
	Orderid string `json:"order_id"`
	Userid string `json:"user_id"`
	Totalamount float64 `json:"total_amount"`
	Shippingaddress entity.Address `json:"shipping_address"`
	Status string `json:"status"`
	Createdat time.Time `json:"created_at"`
}

// NewOrderReadModel 创建Order读模型
func NewOrderReadModel(id string) *OrderReadModel {
	return &OrderReadModel{
		ReadModel: projection.NewReadModel(id, "order"),
	}
}

// ApplyEvent 应用领域事件到读模型
func (m *OrderReadModel) ApplyEvent(event entity.DomainEvent) error {
	switch event.GetEventType() {
	case "OrderCreated":
		return m.applyCreated(event)
	case "OrderUpdated":
		return m.applyUpdated(event)
	case "OrderDeleted":
		return m.applyDeleted(event)
	default:
		return nil // 忽略不相关事件
	}
}

func (m *OrderReadModel) applyCreated(event entity.DomainEvent) error {
	// 从事件数据填充业务字段
	data := event.GetData()
	
	// TODO: 根据实际事件结构填充字段
	// 示例：
	// if name, ok := data["name"]; ok {
	// 	m.Name = name.(string)
	// }
	
	return nil
}

func (m *OrderReadModel) applyUpdated(event entity.DomainEvent) error {
	// 从事件数据更新业务字段
	data := event.GetData()
	
	// TODO: 根据实际事件结构更新字段
	_ = data
	
	return nil
}

func (m *OrderReadModel) applyDeleted(event entity.DomainEvent) error {
	// 标记为已删除或清理数据
	// 可以设置删除标记或清空字段
	return nil
}