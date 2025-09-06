// Email - Value Object
package entity

import (
	"encoding/json"
	"fmt"
	"reflect"
	"regexp"
)

// Email represents a value object for 
type Email struct {
	address string `json:"address"`
	verified bool `json:"verified"`
}

// NewEmail creates a new Email value object
func NewEmail(address string, verified bool) Email {
	return Email {
		address: address,
		verified: verified,
	}
}

// Equals checks if two Email instances are equal
func (v Email) Equals(other Email) bool {
	if !reflect.DeepEqual(v.address, other.address) {
		return false
	}
	if !reflect.DeepEqual(v.verified, other.verified) {
		return false
	}
	return true
}

// String returns string representation
func (v Email) String() string {
	data, _ := json.Marshal(v)
	return string(data)
}

// Validate validates the value object
func (v Email) Validate() error {
	return nil
}