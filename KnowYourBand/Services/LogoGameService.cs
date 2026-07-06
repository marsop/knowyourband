using System.Net.Http.Json;

namespace KnowYourBand.Services;

public class LogoGameService
{
    private readonly HttpClient _http;
    private List<BandLogo> _allLogos = new();
    private Random _random = new Random();

    public int Score { get; private set; } = 0;
    public BandLogo? CurrentLogo { get; private set; }
    public string Feedback { get; private set; } = string.Empty;
    public bool HasGuessed { get; private set; } = false;

    public LogoGameService(HttpClient http)
    {
        _http = http;
    }

    public async Task InitializeAsync()
    {
        var logos = await _http.GetFromJsonAsync<List<BandLogo>>("data/logos.json");
        if (logos != null)
        {
            _allLogos = logos;
            NextLogo();
        }
    }

    public void NextLogo()
    {
        if (_allLogos.Count == 0) return;

        int index = _random.Next(_allLogos.Count);
        CurrentLogo = _allLogos[index];
        Feedback = string.Empty;
        HasGuessed = false;
    }

    public bool CheckGuess(string guess)
    {
        if (CurrentLogo == null || HasGuessed) return false;

        HasGuessed = true;

        // Simple case-insensitive match
        if (string.Equals(CurrentLogo.Name, guess.Trim(), StringComparison.OrdinalIgnoreCase))
        {
            Score++;
            Feedback = "Correct!";
            return true;
        }
        else
        {
            Feedback = $"Incorrect! The correct answer was: {CurrentLogo.Name}";
            return false;
        }
    }
}

public class BandLogo
{
    public string Name { get; set; } = string.Empty;
    public string Logo { get; set; } = string.Empty;
}
