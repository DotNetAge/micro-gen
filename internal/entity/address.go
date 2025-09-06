// Address - Value Object
package entity

import (
	"encoding/json"
	"fmt"
	"reflect"
	"regexp"
)

// Address represents a value object for 
type Address struct {
	street string `json:"street"`
	city string `json:"city"`
	zipCode string `json:"zip_code"`
}

// NewAddress creates a new Address value object
func NewAddress(street string, city string, zipcode string) Address {
	return Address {
		street: street,
		city: city,
		zipCode: zipcode,
	}
}

// Equals checks if two Address instances are equal
func (v Address) Equals(other Address) bool {
	if !reflect.DeepEqual(v.street, other.street) {
		return false
	}
	if !reflect.DeepEqual(v.city, other.city) {
		return false
	}
	if !reflect.DeepEqual(v.zipCode, other.zipCode) {
		return false
	}
	return true
}

// String returns string representation
func (v Address) String() string {
	data, _ := json.Marshal(v)
	return string(data)
}

// Validate validates the value object
func (v Address) Validate() error {
	return nil
}