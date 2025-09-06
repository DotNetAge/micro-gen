package persistence

import (
	"context"
	"sync"

	"test-local/internal/entity/projection"
)

// MemoryOrderRepository 内存实现的Order读模型存储适配器
type MemoryOrderRepository struct {
	mu     sync.RWMutex
	models map[string]*OrderReadModel // id -> model
}

// NewMemoryOrderRepository 创建内存存储适配器
func NewMemoryOrderRepository() *MemoryOrderRepository {
	return &MemoryOrderRepository{
		models: make(map[string]*OrderReadModel),
	}
}

// Save 保存读模型到内存
func (r *MemoryOrderRepository) Save(ctx context.Context, model *OrderReadModel) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	r.models[model.GetID()] = model
	return nil
}

// FindByID 根据ID查找读模型
func (r *MemoryOrderRepository) FindByID(ctx context.Context, id string) (*OrderReadModel, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	if model, ok := r.models[id]; ok {
		return model, nil
	}
	
	return nil, projection.ErrReadModelNotFound
}

// FindAll 查找所有读模型
func (r *MemoryOrderRepository) FindAll(ctx context.Context) ([]*OrderReadModel, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	var result []*OrderReadModel
	for _, model := range r.models {
		result = append(result, model)
	}
	
	return result, nil
}

// Delete 删除读模型
func (r *MemoryOrderRepository) Delete(ctx context.Context, id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	delete(r.models, id)
	return nil
}