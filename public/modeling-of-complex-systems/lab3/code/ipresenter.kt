interface Presenter {
	fun open()
	fun save()
	fun update(src: Experiment)
	fun remove()
	fun create()
}