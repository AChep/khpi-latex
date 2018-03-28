val v = dialog.customView!!
val amp = v.findViewById<EditText>(R.id.amplitude).text.toString()
val wei = v.findViewById<EditText>(R.id.weight).text.toString()
val stf = v.findViewById<EditText>(R.id.stiffness).text.toString()

experiment.apply {
    amplitude = amp.toDoubleOrNull() ?: amplitude
    weight = wei.toDoubleOrNull() ?: weight
    k = stf.toDoubleOrNull() ?: k
}

bind()