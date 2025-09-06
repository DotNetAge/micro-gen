package persistence

import (
	"context"
	"sync"

	"test-local/internal/entity/projection"
)

// MemoryUserRepository 内存实现的User读模型存储适配器
type MemoryUserRepository struct {
	mu     sync.RWMutex
	models map[string]*UserReadModel // id -> model
}

// NewMemoryUserRepository 创建内存存储适配器
func NewMemoryUserRepository() *MemoryUserRepository {
	return &MemoryUserRepository{
		models: make(map[string]*UserReadModel),
	}
}

// Save 保存读模型到内存
func (r *MemoryUserRepository) Save(ctx context.Context, model *UserReadModel) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	r.models[model.GetID()] = model
	return nil
}

// FindByID 根据ID查找读模型
func (r *MemoryUserRepository) FindByID(ctx context.Context, id string) (*UserReadModel, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	if model, ok := r.models[id]; ok {
		return model, nil
	}
	
	return nil, projection.ErrReadModelNotFound
}

// FindAll 查找所有读模型
func (r *MemoryUserRepository) FindAll(ctx context.Context) ([]*UserReadModel, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	var result []*UserReadModel
	for _, model := range r.models {
		result = append(result, model)
	}
	
	return result, nil
}

// Delete 删除读模型
func (r *MemoryUserRepository) Delete(ctx context.Context, id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	delete(r.models, id)
	return nil
}