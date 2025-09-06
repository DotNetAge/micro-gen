package projection

import (
	"context"

	"test-local/internal/entity"
	"test-local/internal/entity/projection"
)

// UserRepository User读模型存储接口
type UserRepository interface {
	Save(ctx context.Context, model *UserReadModel) error
	FindByID(ctx context.Context, id string) (*UserReadModel, error)
	FindAll(ctx context.Context) ([]*UserReadModel, error)
	Delete(ctx context.Context, id string) error
}

// UserProjectionService User投影用例服务
type UserProjectionService struct {
	repo UserRepository
}

// NewUserProjectionService 创建投影服务
func NewUserProjectionService(repo UserRepository) *UserProjectionService {
	return &UserProjectionService{
		repo: repo,
	}
}

// HandleEvent 处理领域事件并更新读模型
func (s *UserProjectionService) HandleEvent(ctx context.Context, event entity.DomainEvent) error {
	// 加载现有读模型
	existing, err := s.repo.FindByID(ctx, event.GetAggregateID())
	if err != nil && err != projection.ErrReadModelNotFound {
		return err
	}
	
	// 创建或获取读模型
	var model *UserReadModel
	if existing != nil {
		model = existing
	} else {
		model = NewUserReadModel(event.GetAggregateID())
	}
	
	// 应用事件
	if err := model.ApplyEvent(event); err != nil {
		return err
	}
	
	// 保存更新
	return s.repo.Save(ctx, model)
}

// GetUser 获取User读模型
func (s *UserProjectionService) GetUser(ctx context.Context, id string) (*UserReadModel, error) {
	return s.repo.FindByID(ctx, id)
}

// GetAllUsers 获取所有User读模型
func (s *UserProjectionService) GetAllUsers(ctx context.Context) ([]*UserReadModel, error) {
	return s.repo.FindAll(ctx)
}