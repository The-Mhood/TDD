#pragma once

// Chapter 1 blockout route contract (WS5). Engine-agnostic validation for
// authoring/export tools; coordinates are neutral gameplay metres (XY plane).

#include <cmath>
#include <cstddef>
#include <string>
#include <vector>

namespace TDD
{
namespace Content
{

struct FTDDRoutePoint
{
    std::string Label;
    double X = 0.0;
    double Y = 0.0;
};

struct FTDDChapterLayout
{
    double MinX = 0.0;
    double MaxX = 0.0;
    double MinY = 0.0;
    double MaxY = 0.0;
    double PathWidth = 0.0;
    FTDDRoutePoint Spawn;
    std::vector<FTDDRoutePoint> Route;
};

struct FTDDLayoutValidation
{
    bool bOk = true;
    std::vector<std::string> Errors;

    void AddError(const std::string& Message)
    {
        bOk = false;
        Errors.push_back(Message);
    }
};

inline FTDDLayoutValidation ValidateChapterLayout(const FTDDChapterLayout& L)
{
    FTDDLayoutValidation Result;
    if (!std::isfinite(L.MinX) || !std::isfinite(L.MaxX) ||
        !std::isfinite(L.MinY) || !std::isfinite(L.MaxY) ||
        !(L.MinX < L.MaxX) || !(L.MinY < L.MaxY))
    {
        Result.AddError("bounds must be finite with positive width and height");
    }
    if (!std::isfinite(L.PathWidth) || !(L.PathWidth > 0.0))
    {
        Result.AddError("path width must be positive");
    }
    if (L.Route.empty())
    {
        Result.AddError("route must contain at least one waypoint");
    }
    if (!std::isfinite(L.Spawn.X) || !std::isfinite(L.Spawn.Y) ||
        L.Spawn.X < L.MinX || L.Spawn.X > L.MaxX ||
        L.Spawn.Y < L.MinY || L.Spawn.Y > L.MaxY)
    {
        Result.AddError("spawn must be finite and lie inside layout bounds");
    }

    std::vector<std::string> Labels;
    for (std::size_t I = 0; I < L.Route.size(); ++I)
    {
        const FTDDRoutePoint& P = L.Route[I];
        if (P.Label.empty())
        {
            Result.AddError("route waypoint label must not be empty");
        }
        for (std::size_t J = 0; J < Labels.size(); ++J)
        {
            if (Labels[J] == P.Label)
            {
                Result.AddError("route waypoint labels must be unique");
                break;
            }
        }
        Labels.push_back(P.Label);
        const double HalfWidth = L.PathWidth * 0.5;
        if (P.X - HalfWidth < L.MinX || P.X + HalfWidth > L.MaxX ||
            P.Y - HalfWidth < L.MinY || P.Y + HalfWidth > L.MaxY)
        {
            Result.AddError("route corridor crosses layout bounds at '" + P.Label + "'");
        }
        if (!std::isfinite(P.X) || !std::isfinite(P.Y))
        {
            Result.AddError("route waypoint coordinates must be finite");
        }
    }
    return Result;
}

inline double RouteLength(const FTDDChapterLayout& L)
{
    double Length = 0.0;
    for (std::size_t I = 1; I < L.Route.size(); ++I)
    {
        const double DX = L.Route[I].X - L.Route[I - 1].X;
        const double DY = L.Route[I].Y - L.Route[I - 1].Y;
        Length += std::sqrt(DX * DX + DY * DY);
    }
    return Length;
}

} // namespace Content
} // namespace TDD
