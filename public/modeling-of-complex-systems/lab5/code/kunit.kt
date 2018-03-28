class Test {

    fun modelCorrectness() {
    	val lst = listOf(
    		Triple(Experiment(1, 1, 1), 0, 1),
    		Triple(Experiment(2.4, 1, 4), 10.428, 0.587),
    		Triple(Experiment(2.4, 1, 4), 17.65, 0.7)
    	)

    	list.forEach {    	
        	val (a, b, c) = it
			val x = Logic.calcPosition(a, b)        	
        	assertTrue { abs(r - c) <= 0.01 }
    	}
    }

}
