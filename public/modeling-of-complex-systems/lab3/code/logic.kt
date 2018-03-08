fun calcSpeed(ex: Experiment, t: Double) : Double {
	val w = calcW(ex)
	return ex.amplitude * cos(w * t)
}

fun calcPosition(ex: Experiment, t: Double) : Double {
	val w = calcW(ex)
	return ex.amplitude * sin(w * t)
}

private fun calcW(ex: Experiment) : Double = ex.k / ex.weight
