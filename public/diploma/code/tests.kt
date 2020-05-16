class GlobeTest : StringSpec() {
    val data = """
            _,       Kyiv, Odessa
            Kharkiv, 478,  -1
            Kyiv,    0,    -1
            Odessa, -1,     0
            Lugansk, 140,  -1
        """.trimIndent()

    val globe = GlobeHipster(DataLoader.assembleGraph(data))

    init {
        "globe should contain Kyiv, Odessa" {
            globe should { it.contains("Kyiv") }
            globe should { it.contains("Odessa") }
        }

        "glove should contain path between Kharkiv and Kyiv" {
            globe.distance("Kharkiv", "Kyiv") shouldBe 478
        }
        
        "glove should not contain path between Kharkiv and Lugansk" {
            globe.distance("Kharkiv", "Lugansk") shouldBe -1
        }
    }
}
