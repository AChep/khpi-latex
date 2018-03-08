@Entity
data class Experiment(
        @PrimaryKey(autoGenerate = true)
        var id: Long = 0,
        var weight: Double = 0.0,
        var amplitude: Double = 0.0,
        var k: Double = 0.0
)