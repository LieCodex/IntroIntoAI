using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject agentPrefab;
    public Transform spawnPoint;
    public Transform target;

    public int populationSize = 100;
    public int dnaLength = 300;
    public float mutationRate = 0.02f;

    private List<Agent> population = new List<Agent>();

    private int step = 0;
    private int generation = 1;

    private Vector2[] bestDNA;

    [SerializeField] private TextMeshProUGUI generationTXT;


    private void Awake()
    {
        Time.timeScale = 10f; // or higher
    }
    void Start()
    {
        bestDNA = LoadBestDNA();

        SpawnPopulation();
    }

    void Update()
    {
        if (step < dnaLength)
        {
            foreach (Agent agent in population)
            {
                agent.MoveAgent();
            }

            step++;
        }
        else
        {
            EndGeneration();
        }
        generationTXT.text = "Generation : " + generation.ToString();
    }

    Vector2[] LoadBestDNA()
    {
        if (!PlayerPrefs.HasKey("DNA_Length"))
            return null;

        int length = PlayerPrefs.GetInt("DNA_Length");

        Vector2[] dna = new Vector2[length];

        for (int i = 0; i < length; i++)
        {
            float x = PlayerPrefs.GetFloat("DNA_X_" + i);
            float y = PlayerPrefs.GetFloat("DNA_Y_" + i);

            dna[i] = new Vector2(x, y);
        }

        return dna;
    }

    void SpawnPopulation()
    {
        population.Clear();

        for (int i = 0; i < populationSize; i++)
        {
            GameObject obj = Instantiate(agentPrefab, spawnPoint.position, Quaternion.identity);
            Agent agent = obj.GetComponent<Agent>();

            Vector2[] dna;

            if (bestDNA == null)
            {
                dna = CreateRandomDNA();
            }
            else
            {
                dna = MutateDNA(bestDNA);
            }

            agent.Initialize(dna, target);
            population.Add(agent);
        }

        step = 0;
    }

    Vector2[] CreateRandomDNA()
    {
        Vector2[] dna = new Vector2[dnaLength];

        for (int i = 0; i < dnaLength; i++)
        {
            dna[i] = Random.insideUnitCircle * 0.1f; 
        }

        return dna;
    }

    Vector2[] MutateDNA(Vector2[] parentDNA)
    {
        Vector2[] dna = new Vector2[parentDNA.Length];

        for (int i = 0; i < parentDNA.Length; i++)
        {
            dna[i] = parentDNA[i];

            if (Random.value < mutationRate)
            {
                dna[i] = Random.insideUnitCircle * 0.1f;
            }
        }

        return dna;
    }

    void EndGeneration()
    {
        Agent bestAgent = null;
        float bestFitness = 0f;

        foreach (Agent agent in population)
        {
            agent.CalculateFitness();

            if (agent.fitness > bestFitness)
            {
                bestFitness = agent.fitness;
                bestAgent = agent;
            }
        }

        // Save best DNA
        bestDNA = bestAgent.CopyDNA();
        SaveBestDNA(bestDNA);
        Debug.Log("Generation: " + generation + " Best Fitness: " + bestFitness);

        // Destroy old agents
        foreach (Agent agent in population)
        {
            Destroy(agent.gameObject);
        }

        generation++;

        SpawnPopulation();
    }

    void SaveBestDNA(Vector2[] dna)
    {
        PlayerPrefs.SetInt("DNA_Length", dna.Length);

        for (int i = 0; i < dna.Length; i++)
        {
            PlayerPrefs.SetFloat("DNA_X_" + i, dna[i].x);
            PlayerPrefs.SetFloat("DNA_Y_" + i, dna[i].y);
        }

        PlayerPrefs.Save();
    }
}