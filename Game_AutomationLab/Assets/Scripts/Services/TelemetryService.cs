using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace Platformer.Services
{
    public class TelemetryService : MonoBehaviour
    {
        private const string ApiUrl = "http://127.0.0.1:8000/events";

        public void SendPlayerDied(string level, Vector2 position)
        {
            StartCoroutine(
                SendPlayerDiedRequest(level, position)
            );
        }

        private IEnumerator SendPlayerDiedRequest(
            string level,
            Vector2 position)
        {
            string json =
                $"{{\"event\":\"player_died\"," +
                $"\"level\":\"{level}\"," +
                $"\"x\":{position.x.ToString(System.Globalization.CultureInfo.InvariantCulture)}," +
                $"\"y\":{position.y.ToString(System.Globalization.CultureInfo.InvariantCulture)}}}";

            using UnityWebRequest request =
                new UnityWebRequest(ApiUrl, "POST");

            byte[] body = System.Text.Encoding.UTF8.GetBytes(json);

            request.uploadHandler = new UploadHandlerRaw(body);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(
                    $"Telemetry error: {request.error}"
                );
            }
            else
            {
                Debug.Log(
                    $"Player death telemetry sent: {json}"
                );
            }
        }

        
    }
}