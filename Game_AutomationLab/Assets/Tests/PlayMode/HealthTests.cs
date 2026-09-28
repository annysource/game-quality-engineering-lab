using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using Platformer.Mechanics;


public class HealthTests
{
    [UnityTest]
    public IEnumerator StartsWithMaxHealth()
    {
        // Arrange
        var gameObject = new GameObject();
        var health = gameObject.AddComponent<Health>();

        // Assert
        Assert.AreEqual(health.maxHP, health.CurrentHP);

        // Cleanup
        Object.DestroyImmediate(gameObject);
        yield return null;
    }
     [UnityTest]
    public IEnumerator DamageReducesHealth()
    {
        // Arrange
        var gameObject = new GameObject();
        var health = gameObject.AddComponent<Health>();

        yield return null;

        // Act
        health.Decrement();

        // Assert
        Assert.AreEqual(0, health.CurrentHP);

        // Cleanup
        Object.Destroy(gameObject);
    }
}
