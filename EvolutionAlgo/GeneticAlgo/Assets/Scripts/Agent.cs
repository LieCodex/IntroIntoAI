using UnityEngine;

public class Agent : MonoBehaviour
{
    public Vector2[] dna;
    public float fitness;

    private int currentStep = 0;
    private Transform target;
    public Rigidbody2D rb;
    bool reachedTarget = false;
    int stepsTaken = 0;
    bool hitWall = false;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>(); // assign Rigidbody2D automatically
    }

    public void Initialize(Vector2[] newDNA, Transform targetTransform)
    {
        dna = newDNA;
        target = targetTransform;
        currentStep = 0;

        // Reset position
        rb.position = transform.position;
    }

    public void MoveAgent()
    {
        if (currentStep >= dna.Length || reachedTarget) return;

        Vector2 newPos = rb.position + dna[currentStep];
        rb.MovePosition(newPos);

        currentStep++;
        stepsTaken++;
    }

    public void CalculateFitness()
    {
        float distance = Vector2.Distance(rb.position, target.position);

        fitness = 1f / (distance + 1f);

        if (reachedTarget)
        {
            // Big reward for reaching the goal
            fitness *= 5f;

            // Reward faster solutions
            fitness += (dna.Length - stepsTaken) * 0.01f;
        }
    }


    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Target"))
        {
            reachedTarget = true;
        }
    }
    public Vector2[] CopyDNA()
    {
        Vector2[] copy = new Vector2[dna.Length];
        for (int i = 0; i < dna.Length; i++)
            copy[i] = dna[i];
        return copy;
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Obstacle"))
        {
            hitWall = true;
            fitness *= 0.5f;
        }
    }
}