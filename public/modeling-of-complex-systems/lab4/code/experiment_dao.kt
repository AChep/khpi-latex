@Dao
interface ExperimentDao {
    @Query("SELECT * FROM Experiment")
    fun experiments(): List<Experiment>
    @Delete
    fun delete(experiment: Experiment)
    @Insert
    fun insert(experiment: Experiment): Long
    @Update
    fun update(experiment: Experiment)
}