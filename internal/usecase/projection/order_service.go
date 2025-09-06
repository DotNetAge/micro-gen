package projection

import (
	"context"

	"test-local/internal/entity"
	"test-local/internal/entity/projection"
)

// OrderRepository Order读模型存储接口
type OrderRepository interface {
	Save(ctx context.Context, model *OrderReadModel) error
	FindByID(ctx context.Context, id string) (*OrderReadModel, error)
	FindAll(ctx context.Context) ([]*OrderReadModel, error)
	Delete(ctx context.Context, id string) error
}

// OrderProjectionService Order投影用例服务
type OrderProjectionService struct {
	repo OrderRepository
}

// NewOrderProjectionService 创建投影服务
func NewOrderProjectionService(repo OrderRepository) *OrderProjectionService {
	return &OrderProjectionService{
		repo: repo,
	}
}

// HandleEvent 处理领域事件并更新读模型
func (s *OrderProjectionService) HandleEvent(ctx context.Context, event entity.DomainEvent) error {
	// 加载现有读模型
	existing, err := s.repo.FindByID(ctx, event.GetAggregateID())
	if err != nil && err != projection.ErrReadModelNotFound {
		return err
	}
	
	// 创建或获取读模型
	var model *OrderReadModel
	if existing != nil {
		model = existing
	} else {
		model = NewOrderReadModel(event.GetAggregateID())
	}
	
	// 应用事件
	if err := model.ApplyEvent(event); err != nil {
		return err
	}
	
	// 保存更新
	return s.repo.Save(ctx, model)
}

// GetOrder 获取Order读模型
func (s *OrderProjectionService) GetOrder(ctx context.Context, id string) (*OrderReadModel, error) {
	return s.repo.FindByID(ctx, id)
}

// GetAllOrders 获取所有Order读模型
func (s *OrderProjectionService) GetAllOrders(ctx context.Context) ([]*OrderReadModel, error) {
	return s.repo.FindAll(ctx)
}