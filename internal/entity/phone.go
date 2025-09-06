// Phone - Value Object
package entity

import (
	"encoding/json"
	"fmt"
	"reflect"
	"regexp"
)

// Phone represents a value object for 
type Phone struct {
	number string `json:"number"`
	countryCode string `json:"country_code"`
}

// NewPhone creates a new Phone value object
func NewPhone(number string, countrycode string) Phone {
	return Phone {
		number: number,
		countryCode: countrycode,
	}
}

// Equals checks if two Phone instances are equal
func (v Phone) Equals(other Phone) bool {
	if !reflect.DeepEqual(v.number, other.number) {
		return false
	}
	if !reflect.DeepEqual(v.countryCode, other.countryCode) {
		return false
	}
	return true
}

// String returns string representation
func (v Phone) String() string {
	data, _ := json.Marshal(v)
	return string(data)
}

// Validate validates the value object
func (v Phone) Validate() error {
	return nil
}