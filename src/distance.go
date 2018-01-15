package main

import "C"

import (
	"github.com/asmarques/geodist"
	"github.com/gonum/floats"
)

//export GoDistance
func GoDistance(lat1 float64, lon1 float64, lat2 float64, lon2 float64) float64 {
	coord1 := geodist.Point{lat1, lon1}
	coord2 := geodist.Point{lat2, lon2}

	dist, _ := geodist.VincentyDistance(coord1, coord2)

	return floats.Round(dist, 4)
}

func main() {}
